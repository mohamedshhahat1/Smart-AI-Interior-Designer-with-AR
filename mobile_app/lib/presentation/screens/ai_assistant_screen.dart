import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class AIAssistantScreen extends StatefulWidget {
  final String roomId;
  const AIAssistantScreen({super.key, required this.roomId});

  @override
  State<AIAssistantScreen> createState() => _AIAssistantScreenState();
}

class _AIAssistantScreenState extends State<AIAssistantScreen> {
  final _messageController = TextEditingController();
  final _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [];
  bool _isTyping = false;

  @override
  void initState() {
    super.initState();
    _messages.add({
      'role': 'assistant',
      'content': 'Hello! I\'m your AI interior design assistant. '
          'I can help you redesign your room, suggest furniture, '
          'pick colors, and more. What would you like to do?',
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _sendMessage() async {
    final text = _messageController.text.trim();
    if (text.isEmpty || _isTyping) return;

    setState(() {
      _messages.add({'role': 'user', 'content': text});
      _isTyping = true;
    });
    _messageController.clear();
    _scrollToBottom();

    try {
      final history = _messages
          .where((m) => m['role'] != null && m['content'] != null)
          .map((m) => {'role': m['role']!, 'content': m['content']!})
          .toList();

      final response = await ApiClient().dio.post('/assistant/chat', data: {
        'room_id': widget.roomId,
        'message': text,
        'conversation_history': history.sublist(0, history.length - 1),
      });

      final data = response.data;
      final assistantMessage = data['message'] as String? ?? 'I couldn\'t process that request.';
      final suggestions = (data['suggestions'] as List?)?.cast<String>() ?? [];

      if (mounted) {
        setState(() {
          _messages.add({'role': 'assistant', 'content': assistantMessage});
          _isTyping = false;
        });

        if (suggestions.isNotEmpty) {
          setState(() {
            _messages.add({
              'role': 'assistant',
              'content': 'Suggestions:\n${suggestions.map((s) => '• $s').join('\n')}',
            });
          });
        }
        _scrollToBottom();
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add({
            'role': 'assistant',
            'content': 'Sorry, I\'m having trouble connecting to the AI service. Please try again.',
          });
          _isTyping = false;
        });
        _scrollToBottom();
      }
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            CircleAvatar(
              radius: 16,
              backgroundColor: AppTheme.primaryColor,
              child: Icon(Icons.auto_awesome, size: 18, color: Colors.white),
            ),
            SizedBox(width: 8),
            Text('Design Assistant'),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isTyping ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length && _isTyping) {
                  return _buildTypingIndicator();
                }
                return _buildMessageBubble(_messages[index]);
              },
            ),
          ),
          _buildInputBar(),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(Map<String, String> message) {
    final isUser = message['role'] == 'user';
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(14),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.78),
        decoration: BoxDecoration(
          color: isUser ? AppTheme.primaryColor : Colors.grey[100],
          borderRadius: BorderRadius.circular(16).copyWith(
            bottomRight: isUser ? const Radius.circular(4) : null,
            bottomLeft: !isUser ? const Radius.circular(4) : null,
          ),
        ),
        child: Text(
          message['content']!,
          style: TextStyle(
            color: isUser ? Colors.white : Colors.black87,
            fontSize: 15,
          ),
        ),
      ),
    );
  }

  Widget _buildTypingIndicator() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.grey[100],
          borderRadius: BorderRadius.circular(16),
        ),
        child: const Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(height: 16, width: 16, child: CircularProgressIndicator(strokeWidth: 2)),
            SizedBox(width: 8),
            Text('Thinking...', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildInputBar() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, -2))],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Ask about your room design...',
                filled: true,
                fillColor: Colors.grey[100],
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(25), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              ),
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          const SizedBox(width: 8),
          CircleAvatar(
            backgroundColor: AppTheme.primaryColor,
            child: IconButton(
              icon: const Icon(Icons.send, color: Colors.white, size: 20),
              onPressed: _sendMessage,
            ),
          ),
        ],
      ),
    );
  }
}
