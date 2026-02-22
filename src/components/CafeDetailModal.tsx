import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
} from 'react-native';
import {BlogAnalysis} from '../types';

interface Props {
  data: BlogAnalysis;
  onClose: () => void;
}

export const CafeDetailModal: React.FC<Props> = ({data, onClose}) => {
  const getScoreColor = (score: number) => {
    if (score >= 3.7) return '#4CAF50';
    if (score >= 2.5) return '#FFC107';
    return '#F44336';
  };

  const openBlogUrl = (url: string) => {
    Linking.openURL(url);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>카페 상세 정보</Text>
        <TouchableOpacity onPress={onClose} style={styles.closeButton}>
          <Text style={styles.closeText}>✕</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* 종합 점수 */}
        <View style={styles.scoreSection}>
          <Text style={styles.sectionTitle}>종합 점수</Text>
          <Text
            style={[styles.totalScore, {color: getScoreColor(data.totalScore)}]}>
            {data.totalScore.toFixed(1)}
          </Text>
        </View>

        {/* 상세 정보 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>상세 정보</Text>
          <InfoRow label="작업 적합도" value={`${data.workScore}/10`} />
          <InfoRow label="콘센트" value={data.outletLevel} />
          <InfoRow label="소음 레벨" value={data.noiseLevel} />
          <InfoRow label="공간감" value={data.spaceLevel} />
          <InfoRow label="테이블 높이" value={data.tableHeight} />
          <InfoRow label="시간 제한" value={data.timeLimit} />
          <InfoRow label="WiFi" value={data.hasWifi ? '있음' : '정보 없음'} />
          <InfoRow
            label="주차"
            value={data.hasParking ? '가능' : '정보 없음'}
          />
        </View>

        {/* 테마 */}
        {data.themes && data.themes.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>테마</Text>
            <View style={styles.themes}>
              {data.themes.map((theme, idx) => (
                <View key={idx} style={styles.themeTag}>
                  <Text style={styles.themeText}>{theme}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* 키워드 */}
        {data.keywords && Object.keys(data.keywords).length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>주요 키워드</Text>
            <View style={styles.keywords}>
              {Object.entries(data.keywords)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10)
                .map(([keyword, count], idx) => (
                  <View key={idx} style={styles.keywordTag}>
                    <Text style={styles.keywordText}>
                      {keyword} ({count})
                    </Text>
                  </View>
                ))}
            </View>
          </View>
        )}

        {/* 블로그 리뷰 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            블로그 리뷰 ({data.blogCount}개)
          </Text>
          {data.blogItems && data.blogItems.length > 0 ? (
            data.blogItems.slice(0, 5).map((blog, idx) => (
              <TouchableOpacity
                key={idx}
                style={styles.blogItem}
                onPress={() => openBlogUrl(blog.url)}>
                <Text style={styles.blogTitle} numberOfLines={1}>
                  {blog.title}
                </Text>
                <Text style={styles.blogDesc} numberOfLines={2}>
                  {blog.description}
                </Text>
              </TouchableOpacity>
            ))
          ) : (
            <Text style={styles.noData}>블로그 리뷰가 없습니다</Text>
          )}
        </View>
      </ScrollView>
    </View>
  );
};

const InfoRow: React.FC<{label: string; value: string}> = ({label, value}) => (
  <View style={styles.infoRow}>
    <Text style={styles.infoLabel}>{label}</Text>
    <Text style={styles.infoValue}>{value}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  closeButton: {
    padding: 4,
  },
  closeText: {
    fontSize: 24,
    color: '#666',
  },
  content: {
    flex: 1,
  },
  scoreSection: {
    alignItems: 'center',
    padding: 24,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  sectionTitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  totalScore: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  section: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  infoLabel: {
    fontSize: 14,
    color: '#666',
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  themes: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  themeTag: {
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  themeText: {
    fontSize: 13,
    color: '#4CAF50',
    fontWeight: '600',
  },
  keywords: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  keywordTag: {
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
  },
  keywordText: {
    fontSize: 12,
    color: '#666',
  },
  blogItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  blogTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  blogDesc: {
    fontSize: 12,
    color: '#666',
    lineHeight: 18,
  },
  noData: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    paddingVertical: 20,
  },
});
