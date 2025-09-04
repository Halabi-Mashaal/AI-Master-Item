#!/usr/bin/env python3
"""
Yamama Cement Warehouse AI Agent - OpenAI Agents Framework Integration
Multi-agent system with specialized warehouse management capabilities
"""
from flask import Flask, jsonify, request
import os
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

app = Flask(__name__)

# ===============================
# ENHANCED MULTI-AGENT SYSTEM
# ===============================

@dataclass
class WarehouseItem:
    """Data model for warehouse items"""
    id: str
    name: str
    quantity: int
    location: str
    category: str
    last_updated: str

@dataclass
class InventoryReport:
    """Data model for inventory reports"""
    total_items: int
    low_stock_items: List[str]
    recent_movements: List[str]
    recommendations: List[str]

class YamamaWarehouseAgent:
    """Base warehouse agent with OpenAI Agents patterns"""
    
    def __init__(self, name: str, instructions: str, tools: List[str] = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.context = {}
    
    async def process(self, query: str, context: Dict = None) -> Dict[str, Any]:
        """Process queries using agent-specific logic"""
        self.context.update(context or {})
        return await self._execute(query)
    
    async def _execute(self, query: str) -> Dict[str, Any]:
        """Override in subclasses"""
        return {"response": "Base agent response", "status": "success"}

class InventoryAgent(YamamaWarehouseAgent):
    """Specialized agent for inventory management"""
    
    def __init__(self):
        super().__init__(
            name="Inventory Manager",
            instructions="Expert in cement inventory tracking, stock levels, and warehouse optimization",
            tools=["inventory_check", "stock_analysis", "reorder_suggestions"]
        )
        # Sample inventory data
        self.inventory = {
            "cement_type_1": {"quantity": 150, "location": "A1-B3", "category": "Portland Cement"},
            "cement_type_2": {"quantity": 75, "location": "A2-B1", "category": "Sulfate Resistant"},
            "cement_type_3": {"quantity": 25, "location": "B1-C2", "category": "Rapid Hardening"}
        }
    
    async def _execute(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['inventory', 'stock', 'مخزون', 'جرد']):
            return self._get_inventory_status()
        elif any(word in query_lower for word in ['low', 'reorder', 'منخفض', 'طلب']):
            return self._check_low_stock()
        elif any(word in query_lower for word in ['location', 'find', 'موقع', 'مكان']):
            return self._find_items(query)
        else:
            return self._general_inventory_help()
    
    def _get_inventory_status(self) -> Dict[str, Any]:
        total_items = sum(item["quantity"] for item in self.inventory.values())
        status = {
            "arabic": f"📊 حالة المخزون الحالية:\n\nإجمالي الكمية: {total_items} طن\n\n" + 
                     "\n".join([f"• {item_id}: {data['quantity']} طن في {data['location']}" 
                               for item_id, data in self.inventory.items()]),
            "english": f"📊 Current Inventory Status:\n\nTotal Quantity: {total_items} tons\n\n" +
                      "\n".join([f"• {item_id}: {data['quantity']} tons at {data['location']}" 
                                for item_id, data in self.inventory.items()])
        }
        
        return {
            "response": status["arabic"] + "\n\n" + status["english"],
            "status": "success",
            "data": {"total_items": total_items, "inventory": self.inventory}
        }
    
    def _check_low_stock(self) -> Dict[str, Any]:
        low_stock = {k: v for k, v in self.inventory.items() if v["quantity"] < 50}
        
        if low_stock:
            response = "⚠️ تحذير المخزون المنخفض | Low Stock Alert:\n\n"
            for item_id, data in low_stock.items():
                response += f"• {item_id}: {data['quantity']} طن (يحتاج إعادة طلب | Needs reorder)\n"
        else:
            response = "✅ جميع المواد متوفرة بكميات كافية | All items are well stocked"
        
        return {
            "response": response,
            "status": "warning" if low_stock else "success",
            "data": {"low_stock_items": low_stock}
        }
    
    def _find_items(self, query: str) -> Dict[str, Any]:
        found_items = []
        for item_id, data in self.inventory.items():
            if any(word in item_id.lower() for word in query.split()):
                found_items.append(f"📍 {item_id}: موجود في {data['location']} | Located at {data['location']}")
        
        if found_items:
            response = "🔍 نتائج البحث | Search Results:\n\n" + "\n".join(found_items)
        else:
            response = "❌ لم يتم العثور على العنصر | Item not found"
        
        return {"response": response, "status": "success", "data": {"found_items": found_items}}
    
    def _general_inventory_help(self) -> Dict[str, Any]:
        return {
            "response": """📦 مدير المخزون | Inventory Manager

يمكنني مساعدتك في:
• فحص حالة المخزون الحالية
• تتبع المواد منخفضة المخزون  
• العثور على مواقع المواد
• تحليل حركة المخزون

I can help you with:
• Check current inventory status
• Track low stock items
• Find item locations  
• Analyze inventory movements""",
            "status": "success"
        }

class LogisticsAgent(YamamaWarehouseAgent):
    """Specialized agent for logistics and transportation"""
    
    def __init__(self):
        super().__init__(
            name="Logistics Coordinator",
            instructions="Expert in cement transportation, delivery scheduling, and logistics optimization",
            tools=["route_planning", "delivery_tracking", "vehicle_management"]
        )
    
    async def _execute(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['delivery', 'transport', 'توصيل', 'نقل']):
            return self._handle_delivery_query()
        elif any(word in query_lower for word in ['route', 'path', 'طريق', 'مسار']):
            return self._suggest_routes()
        elif any(word in query_lower for word in ['schedule', 'timing', 'جدولة', 'وقت']):
            return self._delivery_scheduling()
        else:
            return self._general_logistics_help()
    
    def _handle_delivery_query(self) -> Dict[str, Any]:
        return {
            "response": """🚛 خدمات التوصيل | Delivery Services

الشاحنات المتاحة:
• 3 شاحنات كبيرة (25 طن لكل منها)
• 5 شاحنات متوسطة (15 طن لكل منها)  
• 2 شاحنات صغيرة (8 طن لكل منها)

Available Trucks:
• 3 Large trucks (25 tons each)
• 5 Medium trucks (15 tons each)
• 2 Small trucks (8 tons each)

⏰ مواعيد التوصيل المتاحة: 6:00 ص - 6:00 م
Available delivery hours: 6:00 AM - 6:00 PM""",
            "status": "success"
        }
    
    def _suggest_routes(self) -> Dict[str, Any]:
        return {
            "response": """🗺️ مخطط الطرق | Route Planning

الطرق المُحسَّنة:
• الرياض: الطريق السريع الشرقي (90 دقيقة)
• جدة: طريق مكة السريع (120 دقيقة)  
• الدمام: الطريق الساحلي (45 دقيقة)

Optimized Routes:
• Riyadh: Eastern Highway (90 minutes)
• Jeddah: Makkah Expressway (120 minutes)
• Dammam: Coastal Route (45 minutes)

💡 نصيحة: تجنب ساعات الذروة 7-9 ص و 4-6 م
Tip: Avoid rush hours 7-9 AM & 4-6 PM""",
            "status": "success"
        }
    
    def _delivery_scheduling(self) -> Dict[str, Any]:
        return {
            "response": """📅 جدولة التوصيل | Delivery Scheduling

المواعيد المتاحة اليوم:
✅ 8:00 ص - 10:00 ص
✅ 1:00 م - 3:00 م  
❌ 3:00 م - 5:00 م (محجوز)

Available slots today:
✅ 8:00 AM - 10:00 AM
✅ 1:00 PM - 3:00 PM
❌ 3:00 PM - 5:00 PM (Booked)

📞 للحجز: اتصل بـ 800-YAMAMA
To book: Call 800-YAMAMA""",
            "status": "success"
        }
    
    def _general_logistics_help(self) -> Dict[str, Any]:
        return {
            "response": """🚚 منسق اللوجستيات | Logistics Coordinator

يمكنني مساعدتك في:
• تنسيق مواعيد التوصيل
• تخطيط أفضل الطرق
• إدارة أسطول الشاحنات
• تتبع الشحنات

I can help you with:
• Schedule deliveries
• Plan optimal routes  
• Manage truck fleet
• Track shipments""",
            "status": "success"
        }

class QualityAgent(YamamaWarehouseAgent):
    """Specialized agent for quality control and compliance"""
    
    def __init__(self):
        super().__init__(
            name="Quality Controller",
            instructions="Expert in cement quality standards, testing procedures, and compliance",
            tools=["quality_testing", "compliance_check", "certification_management"]
        )
    
    async def _execute(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['quality', 'test', 'جودة', 'فحص']):
            return self._quality_standards()
        elif any(word in query_lower for word in ['certificate', 'compliance', 'شهادة', 'مطابقة']):
            return self._certification_info()
        elif any(word in query_lower for word in ['standard', 'specification', 'معيار', 'مواصفة']):
            return self._technical_specs()
        else:
            return self._general_quality_help()
    
    def _quality_standards(self) -> Dict[str, Any]:
        return {
            "response": """🔬 معايير الجودة | Quality Standards

اختبارات الجودة الحالية:
✅ قوة الضغط: 42.5 MPa (ممتاز)
✅ زمن الشك الابتدائي: 45 دقيقة
✅ التركيب الكيميائي: مطابق للمعايير

Current Quality Tests:
✅ Compressive Strength: 42.5 MPa (Excellent)
✅ Initial Setting Time: 45 minutes  
✅ Chemical Composition: Standards Compliant

🏆 شهادة الآيزو 9001:2015 سارية
ISO 9001:2015 Certificate Valid""",
            "status": "success"
        }
    
    def _certification_info(self) -> Dict[str, Any]:
        return {
            "response": """📜 الشهادات والمطابقة | Certifications & Compliance

الشهادات السارية:
🏅 ISO 9001:2015 (إدارة الجودة)
🏅 SASO 1001 (المعايير السعودية)
🏅 ASTM C150 (المعايير الأمريكية)
🏅 EN 197-1 (المعايير الأوروبية)

Valid Certifications:
🏅 ISO 9001:2015 (Quality Management)  
🏅 SASO 1001 (Saudi Standards)
🏅 ASTM C150 (American Standards)
🏅 EN 197-1 (European Standards)

📅 تاريخ انتهاء الشهادات: ديسمبر 2025
Certificate expiry: December 2025""",
            "status": "success"
        }
    
    def _technical_specs(self) -> Dict[str, Any]:
        return {
            "response": """⚙️ المواصفات الفنية | Technical Specifications

إسمنت بورتلاندي عادي:
• المقاومة: 42.5 N/mm² بعد 28 يوم
• النعومة: 350 م²/كغ
• زمن الشك: 30-600 دقيقة
• التمدد: < 10 مم

Ordinary Portland Cement:
• Strength: 42.5 N/mm² after 28 days
• Fineness: 350 m²/kg  
• Setting Time: 30-600 minutes
• Expansion: < 10 mm

🌡️ درجة حرارة التخزين: 5-35°C
Storage Temperature: 5-35°C""",
            "status": "success"
        }
    
    def _general_quality_help(self) -> Dict[str, Any]:
        return {
            "response": """🎯 مراقب الجودة | Quality Controller

يمكنني مساعدتك في:
• فحص معايير الجودة  
• التحقق من الشهادات
• المواصفات الفنية
• إجراءات الاختبار

I can help you with:
• Check quality standards
• Verify certifications  
• Technical specifications
• Testing procedures""",
            "status": "success"
        }

# ===============================
# AGENT ORCHESTRATOR (Manager Pattern)
# ===============================

class YamamaAgentOrchestrator:
    """Central orchestrator using OpenAI Agents manager pattern"""
    
    def __init__(self):
        self.agents = {
            "inventory": InventoryAgent(),
            "logistics": LogisticsAgent(), 
            "quality": QualityAgent()
        }
        self.conversation_history = []
    
    async def route_query(self, user_query: str, context: Dict = None) -> Dict[str, Any]:
        """Route queries to appropriate specialized agents"""
        query_lower = user_query.lower()
        
        # Agent routing logic
        if any(word in query_lower for word in ['inventory', 'stock', 'مخزون', 'جرد', 'quantity', 'كمية']):
            agent = self.agents["inventory"]
        elif any(word in query_lower for word in ['delivery', 'transport', 'logistics', 'توصيل', 'نقل', 'شحن']):
            agent = self.agents["logistics"]
        elif any(word in query_lower for word in ['quality', 'test', 'standard', 'جودة', 'فحص', 'معيار']):
            agent = self.agents["quality"]
        else:
            # Default to general warehouse help
            return self._general_warehouse_help(user_query)
        
        # Execute with specialized agent
        try:
            result = await agent.process(user_query, context or {})
            
            # Add orchestrator metadata
            result["agent_used"] = agent.name
            result["timestamp"] = datetime.now().isoformat()
            
            # Update conversation history
            self.conversation_history.append({
                "query": user_query,
                "agent": agent.name,
                "response": result["response"],
                "timestamp": result["timestamp"]
            })
            
            return result
            
        except Exception as e:
            return {
                "response": f"عذراً، حدث خطأ في النظام | Sorry, system error: {str(e)}",
                "status": "error",
                "agent_used": "error_handler"
            }
    
    def _general_warehouse_help(self, query: str) -> Dict[str, Any]:
        """General warehouse assistance"""
        return {
            "response": """🏭 مرحباً بك في نظام يمامة الذكي للمستودعات
Welcome to Yamama Smart Warehouse System

🤖 الوكلاء المتخصصون المتاحون | Available Specialized Agents:

📦 مدير المخزون | Inventory Manager
- فحص المخزون والكميات | Check stock and quantities
- تتبع المواد المنخفضة | Track low stock items
- مواقع التخزين | Storage locations

🚚 منسق اللوجستيات | Logistics Coordinator  
- جدولة التوصيل | Delivery scheduling
- تخطيط الطرق | Route planning
- إدارة الأسطول | Fleet management

🔬 مراقب الجودة | Quality Controller
- معايير الجودة | Quality standards  
- الشهادات والمطابقة | Certifications & compliance
- الاختبارات الفنية | Technical testing

💬 اكتب سؤالك وسيتم توجيهك للوكيل المناسب
Write your question and you'll be routed to the appropriate agent""",
            "status": "success",
            "agent_used": "orchestrator"
        }

# Initialize the orchestrator
warehouse_orchestrator = YamamaAgentOrchestrator()

HTML_TEMPLATE = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yamama AI</title>
    <style>
        body{font-family:Arial;background:#4CAF50;padding:20px;color:white}
        .container{max-width:600px;margin:0 auto;text-align:center}
        .logo{font-size:60px;margin:20px}
        h1{margin:20px 0}
        .chat{background:white;color:#333;padding:20px;border-radius:10px;margin:20px 0;max-height:400px;overflow-y:auto}
        input{width:80%;padding:10px;margin:10px;border:1px solid #ddd;border-radius:5px}
        button{background:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer}
        .message{margin:10px 0;padding:10px;background:#f0f0f0;border-radius:5px}
        .user-message{background:#e3f2fd;text-align:right}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🏭</div>
        <h1>Yamama Cement AI Agent</h1>
        <p>Your intelligent assistant for cement and warehouse management</p>
        <div class="chat" id="chat">
            <div class="message">مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت!</div>
        </div>
        <input type="text" id="msg" placeholder="اكتب رسالتك هنا..." onkeypress="if(event.key==='Enter')send()">
        <button onclick="send()">إرسال</button>
    </div>
    <script>
        function send(){
            var msg=document.getElementById('msg').value.trim();
            if(!msg)return;
            
            document.getElementById('chat').innerHTML+='<div class="message user-message">'+msg+'</div>';
            document.getElementById('msg').value='';
            
            fetch('/chat',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({message:msg})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('chat').innerHTML+='<div class="message">'+data.response+'</div>';
                document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
            })
            .catch(error => {
                document.getElementById('chat').innerHTML+='<div class="message">خطأ في الاتصال - Connection Error</div>';
            });
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'yamama-warehouse-ai',
        'version': '2.0-multiagent',
        'agents': ['inventory', 'logistics', 'quality']
    })

@app.route('/test')
def test():
    return jsonify({
        'message': 'Yamama Multi-Agent Warehouse System is operational!',
        'status': 'success',
        'arabic': 'نظام يمامة متعدد الوكلاء للمستودعات يعمل بشكل ممتاز!',
        'agents_available': len(warehouse_orchestrator.agents)
    })

@app.route('/agents')
def list_agents():
    """List all available agents"""
    agents_info = {}
    for agent_id, agent in warehouse_orchestrator.agents.items():
        agents_info[agent_id] = {
            'name': agent.name,
            'instructions': agent.instructions,
            'tools': agent.tools
        }
    
    return jsonify({
        'agents': agents_info,
        'total_agents': len(agents_info),
        'orchestrator': 'YamamaAgentOrchestrator'
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        if not data:
            return jsonify({
                'response': 'لم يتم استلام رسالة - No message received',
                'status': 'error'
            })
        
        message = str(data.get('message', '')).strip()
        
        if not message:
            return jsonify({
                'response': 'الرسالة فارغة - Empty message',
                'status': 'error'
            })
        
        # Route to appropriate agent using orchestrator
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                warehouse_orchestrator.route_query(message)
            )
            return jsonify(result)
        finally:
            loop.close()
        
    except Exception as e:
        return jsonify({
            'response': f'خطأ في النظام - System error: {str(e)}',
            'status': 'error',
            'agent_used': 'error_handler'
        }), 500

@app.route('/history')
def get_history():
    """Get conversation history"""
    return jsonify({
        'history': warehouse_orchestrator.conversation_history[-10:],  # Last 10 conversations
        'total_conversations': len(warehouse_orchestrator.conversation_history)
    })

if __name__ == '__main__':
    print("🚀 YAMAMA MULTI-AGENT WAREHOUSE SYSTEM - STARTING...")
    print("📦 Inventory Agent: Ready")
    print("🚚 Logistics Agent: Ready") 
    print("🔬 Quality Agent: Ready")
    print("🎯 Orchestrator: Ready")
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
