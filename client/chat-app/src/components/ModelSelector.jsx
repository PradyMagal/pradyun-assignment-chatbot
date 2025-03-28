import { useState, useEffect } from 'react';
import { fetchOpenAIModels, fetchAnthropicModels } from '../services/api';
import './ModelSelector.css';

const ModelSelector = ({ onModelSelect }) => {
  const [provider, setProvider] = useState('openai');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [loading, setLoading] = useState(false);

  // Keep track of previous provider to detect changes
  const [prevProvider, setPrevProvider] = useState(provider);
  
  useEffect(() => {
    const loadModels = async () => {
      setLoading(true);
      try {
        let modelData;
        if (provider === 'openai') {
          modelData = await fetchOpenAIModels();
        } else {
          modelData = await fetchAnthropicModels();
        }
        setModels(modelData);
        
        // Check if we're changing providers
        const isProviderChange = prevProvider !== provider;
        setPrevProvider(provider);
        
        // Only set the selected model if it's not already set or if we're changing providers
        if (modelData.length > 0) {
          if (isProviderChange || !selectedModel) {
            console.log(`Setting model to ${modelData[0].id}`);
            setSelectedModel(modelData[0].id);
            onModelSelect(modelData[0].id, provider);
          }
        }
      } catch (error) {
        console.error('Error loading models:', error);
      } finally {
        setLoading(false);
      }
    };

    loadModels();
  }, [provider, onModelSelect]);

  const handleProviderChange = (newProvider) => {
    console.log(`Changing provider to: ${newProvider}`);
    setProvider(newProvider);
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
    onModelSelect(e.target.value, provider);
  };

  return (
    <div className="model-selector">
      <div className="form-group">
        <label>Select Provider</label>
        <div className="provider-toggle">
          <div 
            className={`provider-option ${provider === 'openai' ? 'active' : ''}`}
            onClick={() => handleProviderChange('openai')}
          >
            OpenAI
          </div>
          <div 
            className={`provider-option ${provider === 'anthropic' ? 'active' : ''}`}
            onClick={() => handleProviderChange('anthropic')}
          >
            Anthropic
          </div>
          <div className={`toggle-slider ${provider}`}></div>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="model-select">Select Model</label>
        <select 
          id="model-select"
          value={selectedModel} 
          onChange={handleModelChange}
          disabled={loading || models.length === 0}
        >
          {loading ? (
            <option value="">Loading models...</option>
          ) : models.length === 0 ? (
            <option value="">No models available</option>
          ) : (
            <>
              {/* Add a default option */}
              {!selectedModel && <option value="">Select a model</option>}
              
              {/* Map through available models */}
              {models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name}
                </option>
              ))}
            </>
          )}
        </select>
      </div>
    </div>
  );
};

export default ModelSelector;
