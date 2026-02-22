import AsyncStorage from '@react-native-async-storage/async-storage';
import {BlogAnalysis} from '../types';

const CACHE_VERSION = 'v18';
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24시간

interface CacheData {
  data: BlogAnalysis;
  timestamp: number;
  version: string;
}

export const getCachedData = async (
  cafeName: string,
  address: string,
): Promise<BlogAnalysis | null> => {
  try {
    const key = `cafe_${CACHE_VERSION}_${cafeName}_${address}`;
    const cached = await AsyncStorage.getItem(key);

    if (cached) {
      const cacheData: CacheData = JSON.parse(cached);
      if (
        Date.now() - cacheData.timestamp < CACHE_DURATION &&
        cacheData.version === CACHE_VERSION
      ) {
        return cacheData.data;
      }
    }
    return null;
  } catch (error) {
    console.error('Cache read error:', error);
    return null;
  }
};

export const setCachedData = async (
  cafeName: string,
  address: string,
  data: BlogAnalysis,
): Promise<void> => {
  try {
    const key = `cafe_${CACHE_VERSION}_${cafeName}_${address}`;
    const cacheData: CacheData = {
      data,
      timestamp: Date.now(),
      version: CACHE_VERSION,
    };
    await AsyncStorage.setItem(key, JSON.stringify(cacheData));
  } catch (error) {
    console.error('Cache write error:', error);
  }
};

export const clearOldCache = async (): Promise<void> => {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const oldKeys = keys.filter(
      key => key.startsWith('cafe_') && !key.startsWith(`cafe_${CACHE_VERSION}_`),
    );
    if (oldKeys.length > 0) {
      await AsyncStorage.multiRemove(oldKeys);
      console.log(`Cleared ${oldKeys.length} old cache entries`);
    }
  } catch (error) {
    console.error('Clear old cache error:', error);
  }
};
