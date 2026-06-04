import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';

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

  void _sendMessage() {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add({'role': 'user', 'content': text});
      _isTyping = true;
    });
    _messageController.clear();
    _scrollToBottom();

    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _messages.add({
            'role': 'assistant',
            'content': _getAssistantResponse(text),
          });
          _isTyping = false;
        });
        _scrollToBottom();
      }
    });
  }

  String _getAssistantResponse(String message) {
    final lower = message.toLowerCase();
    if (lower.contains('larger') || lower.contains('bigger') || lower.contains('space')) {
      return 'To make your room look larger:\n\n'
          '1. Use light, neutral wall colors (white, cream, light gray)\n'
          '2. Add mirrors to create depth\n'
          '3. Choose furniture with exposed legs\n'
          '4. Maximize natural light with sheer curtains\n'
          '5. Use a monochromatic color scheme\n\n'
          'Would you like me to generate a design with these changes?';
    } else if (lower.contains('cozy') || lower.contains('warm')) {
      return 'For a cozy atmosphere:\n\n'
          '1. Add warm lighting with dimmers\n'
          '2. Layer textiles - throws, cushions, rugs\n'
          '3. Use warm tones (amber, terracotta)\n'
          '4. Include natural materials (wood, wool)\n'
          '5. Create intimate seating areas\n\n'
          'Shall I create a preview with these elements?';
    } else if (lower.contains('color') || lower.contains('palette')) {
      return 'Here are popular color palettes:\n\n'
          'Scandinavian: White + Light Wood + Sage Green\n'
          'Modern: Charcoal + White + Gold Accents\n'
          'Coastal: Navy Blue + Sandy Beige + White\n'
          'Bohemian: Terracotta + Teal + Mustard\n\n'
          'Which palette interests you?';
    } else if (lower.contains('budget') || lower.contains('cost') || lower.contains('cheap')) {
      return 'Budget-friendly design tips:\n\n'
          '1. Repaint walls for the biggest impact (~\$200-400)\n'
          '2. Rearrange existing furniture\n'
          '3. Add affordable accessories (pillows, throws)\n'
          '4. DIY artwork or gallery wall\n'
          '5. Shop second-hand for statement pieces\n\n'
          'What is your budget range?';
    }
    return 'Great question! Based on your room analysis, I recommend:\n\n'
        '1. Follow the 60-30-10 color rule\n'
        '2. Create a clear focal point\n'
        '3. Balance furniture scale with room size\n'
        '4. Layer lighting (ambient + task + accent)\n'
        '5. Add texture variety for visual interest\n\n'
        'Would you like specific suggestions for any of these?';
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
