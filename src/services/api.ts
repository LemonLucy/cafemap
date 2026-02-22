import axios from 'axios';
import {BlogAnalysis, Cafe} from '../types';

const API_BASE_URL = 'http://localhost:5000'; // 실제 서버 URL로 변경 필요
const KAKAO_API_KEY = '297844bdfecc46774483cc747fc2bfe6';

export const searchCafes = async (
  query: string,
  x: number,
  y: number,
  radius: number = 2000,
): Promise<Cafe[]> => {
  try {
    const response = await axios.get(
      'https://dapi.kakao.com/v2/local/search/keyword.json',
      {
        headers: {
          Authorization: `KakaoAK ${KAKAO_API_KEY}`,
        },
        params: {
          query: `${query} 카페`,
          x,
          y,
          radius,
          size: 15,
          sort: 'distance',
        },
      },
    );

    return response.data.documents.map((doc: any) => ({
      name: doc.place_name,
      address: doc.address_name,
      x: parseFloat(doc.x),
      y: parseFloat(doc.y),
      distance: parseInt(doc.distance),
      place_url: doc.place_url,
      phone: doc.phone,
      category_name: doc.category_name,
    }));
  } catch (error) {
    console.error('Kakao API Error:', error);
    return [];
  }
};

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

export const clearCache = async (): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/api/clear-cache`);
  } catch (error) {
    console.error('Clear cache error:', error);
  }
};
