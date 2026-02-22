import React, {useState, useEffect, useRef} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  FlatList,
  ActivityIndicator,
  Alert,
  SafeAreaView,
  TouchableOpacity,
  Modal,
  Platform,
  PermissionsAndroid,
} from 'react-native';
import Geolocation from 'react-native-geolocation-service';
import {CafeListItem} from '../components/CafeListItem';
import {CafeDetailModal} from '../components/CafeDetailModal';
import {searchCafes, analyzeCafe} from '../services/api';
import {getCachedData, setCachedData, clearOldCache} from '../utils/cache';
import {Cafe, BlogAnalysis, UserLocation} from '../types';

export const MapScreen: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('Coffee');
  const [cafes, setCafes] = useState<Cafe[]>([]);
  const [cafeAnalysis, setCafeAnalysis] = useState<{
    [key: string]: BlogAnalysis;
  }>({});
  const [loading, setLoading] = useState(false);
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);
  const [selectedCafe, setSelectedCafe] = useState<Cafe | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [sortBy, setSortBy] = useState<'score-high' | 'score-low' | 'distance'>(
    'score-high',
  );

  useEffect(() => {
    requestLocationPermission();
    clearOldCache();
  }, []);

  const requestLocationPermission = async () => {
    if (Platform.OS === 'android') {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        getCurrentLocation();
      }
    } else {
      getCurrentLocation();
    }
  };

  const getCurrentLocation = () => {
    Geolocation.getCurrentPosition(
      position => {
        setUserLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
        handleSearch(
          searchQuery,
          position.coords.longitude,
          position.coords.latitude,
        );
      },
      error => {
        console.error(error);
        // 기본 위치 (서울 시청)
        setUserLocation({latitude: 37.5665, longitude: 126.978});
        handleSearch(searchQuery, 126.978, 37.5665);
      },
      {enableHighAccuracy: true, timeout: 15000, maximumAge: 10000},
    );
  };

  const handleSearch = async (query: string, x?: number, y?: number) => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const searchX = x || userLocation?.longitude || 126.978;
      const searchY = y || userLocation?.latitude || 37.5665;

      const results = await searchCafes(query, searchX, searchY);
      setCafes(results);

      // 각 카페 분석 시작
      results.forEach(cafe => loadCafeAnalysis(cafe));
    } catch (error) {
      Alert.alert('오류', '카페 검색에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const loadCafeAnalysis = async (cafe: Cafe) => {
    const cacheKey = `${cafe.name}_${cafe.address}`;

    // 캐시 확인
    const cached = await getCachedData(cafe.name, cafe.address);
    if (cached) {
      setCafeAnalysis(prev => ({...prev, [cacheKey]: cached}));
      return;
    }

    // API 호출
    try {
      const analysis = await analyzeCafe(cafe.name, cafe.address);
      setCafeAnalysis(prev => ({...prev, [cacheKey]: analysis}));
      await setCachedData(cafe.name, cafe.address, analysis);
    } catch (error) {
      console.error('Analysis error:', cafe.name, error);
    }
  };

  const handleCafePress = (cafe: Cafe) => {
    setSelectedCafe(cafe);
    setModalVisible(true);
  };

  const getSortedCafes = () => {
    const cafesWithAnalysis = cafes.map(cafe => ({
      cafe,
      analysis: cafeAnalysis[`${cafe.name}_${cafe.address}`],
    }));

    switch (sortBy) {
      case 'score-high':
        return cafesWithAnalysis.sort(
          (a, b) => (b.analysis?.totalScore || 0) - (a.analysis?.totalScore || 0),
        );
      case 'score-low':
        return cafesWithAnalysis.sort(
          (a, b) => (a.analysis?.totalScore || 0) - (b.analysis?.totalScore || 0),
        );
      case 'distance':
        return cafesWithAnalysis.sort(
          (a, b) => (a.cafe.distance || 0) - (b.cafe.distance || 0),
        );
      default:
        return cafesWithAnalysis;
    }
  };

  const selectedAnalysis = selectedCafe
    ? cafeAnalysis[`${selectedCafe.name}_${selectedCafe.address}`]
    : null;

  return (
    <SafeAreaView style={styles.container}>
      {/* 검색바 */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          value={searchQuery}
          onChangeText={setSearchQuery}
          onSubmitEditing={() => handleSearch(searchQuery)}
          placeholder="카페 검색..."
          returnKeyType="search"
        />
        <TouchableOpacity
          style={styles.searchButton}
          onPress={() => handleSearch(searchQuery)}>
          <Text style={styles.searchButtonText}>검색</Text>
        </TouchableOpacity>
      </View>

      {/* 정렬 버튼 */}
      <View style={styles.sortContainer}>
        <Text style={styles.cafeCount}>
          {cafes.length}개 카페 | 분석 완료:{' '}
          {Object.keys(cafeAnalysis).length}개
        </Text>
        <View style={styles.sortButtons}>
          <SortButton
            label="평점 높은순"
            active={sortBy === 'score-high'}
            onPress={() => setSortBy('score-high')}
          />
          <SortButton
            label="평점 낮은순"
            active={sortBy === 'score-low'}
            onPress={() => setSortBy('score-low')}
          />
          <SortButton
            label="거리순"
            active={sortBy === 'distance'}
            onPress={() => setSortBy('distance')}
          />
        </View>
      </View>

      {/* 카페 리스트 */}
      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>카페 검색 중...</Text>
        </View>
      ) : (
        <FlatList
          data={getSortedCafes()}
          keyExtractor={(item, index) => `${item.cafe.name}_${index}`}
          renderItem={({item}) => (
            <CafeListItem
              cafe={item.cafe}
              analysis={item.analysis}
              onPress={() => handleCafePress(item.cafe)}
            />
          )}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyText}>검색 결과가 없습니다</Text>
            </View>
          }
        />
      )}

      {/* 상세 정보 모달 */}
      <Modal
        visible={modalVisible}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}>
        {selectedCafe && selectedAnalysis ? (
          <CafeDetailModal
            data={selectedAnalysis}
            onClose={() => setModalVisible(false)}
          />
        ) : (
          <View style={styles.modalLoading}>
            <ActivityIndicator size="large" color="#4CAF50" />
            <Text style={styles.loadingText}>분석 중...</Text>
          </View>
        )}
      </Modal>
    </SafeAreaView>
  );
};

const SortButton: React.FC<{
  label: string;
  active: boolean;
  onPress: () => void;
}> = ({label, active, onPress}) => (
  <TouchableOpacity
    style={[styles.sortButton, active && styles.sortButtonActive]}
    onPress={onPress}>
    <Text style={[styles.sortButtonText, active && styles.sortButtonTextActive]}>
      {label}
    </Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  searchContainer: {
    flexDirection: 'row',
    padding: 12,
    gap: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  searchInput: {
    flex: 1,
    height: 44,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
  },
  searchButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    borderRadius: 8,
    justifyContent: 'center',
  },
  searchButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  sortContainer: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  cafeCount: {
    fontSize: 13,
    color: '#666',
    marginBottom: 8,
  },
  sortButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  sortButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#f5f5f5',
  },
  sortButtonActive: {
    backgroundColor: '#4CAF50',
  },
  sortButtonText: {
    fontSize: 12,
    color: '#666',
  },
  sortButtonTextActive: {
    color: '#fff',
    fontWeight: '600',
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
  empty: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
  },
  modalLoading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
});
