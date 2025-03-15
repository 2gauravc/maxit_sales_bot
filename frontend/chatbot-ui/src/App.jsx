import { useState, useEffect, useRef } from "react";
import { Send, Plus } from "lucide-react";

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  const [pastChats, setPastChats] = useState([]); // Placeholder for future chats

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    
    // Simulate bot response
    setTimeout(() => {
      setMessages([...newMessages, { text: "I'm just a bot!", sender: "bot" }]);
    }, 1000);
  };

  return (
    <div className="flex h-screen w-full bg-gray-100">
      {/* Dedicated Left Panel for Past Chats */}
      <div className="w-1/4 h-full bg-white shadow-lg p-4 overflow-auto border-r border-gray-300 flex flex-col">
        <h2 className="text-lg font-semibold mb-4">Past Chats</h2>
        {pastChats.length === 0 ? (
          <p className="text-gray-500">No past chats yet</p>
        ) : (
          pastChats.map((chat, index) => (
            <div key={index} className="p-2 border-b cursor-pointer hover:bg-gray-200">
              Chat {index + 1}
            </div>
          ))
        )}
      </div>

      {/* Right Panel with Chat History and Input Section */}
      <div className="flex flex-col w-3/4 h-full">
        {/* Chat History */}
        <div className="flex-grow overflow-auto p-4 bg-white rounded-2xl shadow-lg flex flex-col">
          {messages.map((msg, index) => (
            <div key={index} className={`my-2 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`p-3 rounded-lg max-w-xs ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* User Input Section */}
        <div className="bg-white p-3 rounded-2xl shadow-md flex space-x-2 border-t border-gray-300 items-center">
          <button className="bg-gray-300 text-black p-2 rounded-lg flex items-center hover:bg-gray-400">
            <Plus size={24} />
          </button>
          <input
            className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
          />
          <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-lg flex items-center hover:bg-blue-600">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
