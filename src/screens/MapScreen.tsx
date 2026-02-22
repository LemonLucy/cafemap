import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Alert,
  SafeAreaView,
} from 'react-native';
import {CafeInfo} from '../components/CafeInfo';
import {analyzeCafe} from '../services/api';
import {BlogAnalysis} from '../types';

export const MapScreen: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [cafeData, setCafeData] = useState<BlogAnalysis | null>(null);

  // 테스트용 카페 데이터 로드
  const loadTestCafe = async () => {
    setLoading(true);
    try {
      const data = await analyzeCafe('스타벅스 강남점', '서울 강남구');
      setCafeData(data);
    } catch (error) {
      Alert.alert('오류', '카페 정보를 불러올 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>CoffeeMap</Text>
      </View>

      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>카페 정보 분석 중...</Text>
        </View>
      ) : cafeData ? (
        <CafeInfo data={cafeData} />
      ) : (
        <View style={styles.placeholder}>
          <Text style={styles.placeholderText}>
            지도 기능은 추후 추가됩니다
          </Text>
          <Text style={styles.placeholderSubtext}>
            카카오맵 SDK 연동 필요
          </Text>
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    color: '#666',
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  placeholderText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 8,
  },
  placeholderSubtext: {
    fontSize: 14,
    color: '#999',
  },
});
