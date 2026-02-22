import axios from 'axios';
import {BlogAnalysis} from '../types';

const API_BASE_URL = 'http://localhost:5000'; // 나중에 실제 서버 URL로 변경

export const analyzeCafe = async (
  name: string,
  address: string,
): Promise<BlogAnalysis> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/blog-search`, {
      name,
      address,
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
