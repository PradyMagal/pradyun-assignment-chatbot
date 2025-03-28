import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchOpenAIModels = async () => {
  try {
    const response = await axios.get(`${API_URL}/openai/models`);
    return response.data.data;
  } catch (error) {
    console.error('Error fetching OpenAI models:', error);
    throw error;
  }
};

export const fetchAnthropicModels = async () => {
  try {
    const response = await axios.get(`${API_URL}/anthropic/models`);
    return response.data.data;
  } catch (error) {
    console.error('Error fetching Anthropic models:', error);
    throw error;
  }
};

export const generateOpenAIResponse = async (model, userPrompt, systemPrompt = '') => {
  try {
    const response = await axios.post(`${API_URL}/openai/generate`, {
      model,
      prompt: userPrompt,
      system_prompt: systemPrompt,
    });
    return response.data.data;
  } catch (error) {
    console.error('Error generating OpenAI response:', error);
    throw error;
  }
};

export const generateAnthropicResponse = async (model, userPrompt, systemPrompt = '') => {
  try {
    const response = await axios.post(`${API_URL}/anthropic/generate`, {
      model,
      prompt: userPrompt,
      system_prompt: systemPrompt,
    });
    return response.data.data;
  } catch (error) {
    console.error('Error generating Anthropic response:', error);
    throw error;
  }
};
