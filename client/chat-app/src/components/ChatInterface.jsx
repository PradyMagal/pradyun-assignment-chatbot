import { useState } from 'react';
import { generateOpenAIResponse, generateAnthropicResponse } from '../services/api';
import './ChatInterface.css';

const ChatInterface = ({ selectedModel, provider }) => {
  const [systemPrompt, setSystemPrompt] = useState('');
  const [userPrompt, setUserPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted', { systemPrompt, userPrompt, selectedModel, provider });
    
    if (!userPrompt.trim() || !selectedModel) {
      console.log('Missing user prompt or model, not submitting');
      return;
    }

    setLoading(true);
    try {
      console.log(`Generating response with ${provider} model: ${selectedModel}`);
      let responseData;
      if (provider === 'openai') {
        responseData = await generateOpenAIResponse(selectedModel, userPrompt, systemPrompt);
      } else {
        responseData = await generateAnthropicResponse(selectedModel, userPrompt, systemPrompt);
      }
      console.log('Response received:', responseData);
      setResponse(responseData.response);
    } catch (error) {
      console.error('Error generating response:', error);
      setResponse('Error: Failed to generate response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-interface ${provider === 'openai' ? 'openai-theme' : 'anthropic-theme'}`}>
      <form onSubmit={handleSubmit} className="prompt-form">
        <div className="form-group">
          <label htmlFor="system-prompt-input">System Prompt (Optional)</label>
          <textarea
            id="system-prompt-input"
            className="form-control system-prompt"
            rows={3}
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
            placeholder="Enter system instructions here (e.g., 'You are a helpful assistant specialized in...')"
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="user-prompt-input">User Prompt</label>
          <textarea
            id="user-prompt-input"
            className="form-control user-prompt"
            rows={6}
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            placeholder="Enter your prompt here..."
            disabled={loading}
          />
        </div>
        
        <button 
          className="generate-btn"
          type="submit" 
          disabled={loading || !selectedModel || !userPrompt.trim()}
        >
          {loading ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <span>Generating...</span>
            </div>
          ) : (
            'Generate Response'
          )}
        </button>
      </form>

      {response && (
        <div className="response-card">
          <div className="response-header">Response</div>
          <div className="response-body">
            <pre className="response-text">
              {response}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
