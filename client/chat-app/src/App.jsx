import { useState } from 'react';
import ModelSelector from './components/ModelSelector';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [selectedModel, setSelectedModel] = useState('');
  const [provider, setProvider] = useState('openai');

  const handleModelSelect = (model, providerName) => {
    setSelectedModel(model);
    setProvider(providerName);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Chat Interface</h1>
        <p>Interact with OpenAI and Anthropic models</p>
      </header>
      
      <main className="app-content">
        <ModelSelector onModelSelect={handleModelSelect} />
        <ChatInterface selectedModel={selectedModel} provider={provider} />
      </main>
      
      <footer className="app-footer">
        <p>Created by Pradyun Magal</p>
      </footer>
    </div>
  );
}

export default App;
