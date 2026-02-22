import React from 'react';
import {View, Text, StyleSheet, ScrollView} from 'react-native';
import {BlogAnalysis} from '../types';

interface Props {
  data: BlogAnalysis;
}

export const CafeInfo: React.FC<Props> = ({data}) => {
  const getScoreColor = (score: number) => {
    if (score >= 3.7) return '#4CAF50';
    if (score >= 2.5) return '#FFC107';
    return '#F44336';
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>종합 점수</Text>
        <Text style={[styles.score, {color: getScoreColor(data.totalScore)}]}>
          {data.totalScore.toFixed(1)}
        </Text>
      </View>

      <View style={styles.section}>
        <InfoRow label="작업 적합도" value={`${data.workScore}/10`} />
        <InfoRow label="콘센트" value={data.outletLevel} />
        <InfoRow label="소음 레벨" value={data.noiseLevel} />
        <InfoRow label="공간감" value={data.spaceLevel} />
        <InfoRow label="WiFi" value={data.hasWifi ? '있음' : '정보 없음'} />
        <InfoRow label="블로그 리뷰" value={`${data.blogCount}개`} />
      </View>

      {data.description && (
        <View style={styles.section}>
          <Text style={styles.description}>{data.description}</Text>
        </View>
      )}
    </ScrollView>
  );
};

const InfoRow: React.FC<{label: string; value: string}> = ({label, value}) => (
  <View style={styles.row}>
    <Text style={styles.label}>{label}</Text>
    <Text style={styles.value}>{value}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 16,
    color: '#666',
    marginBottom: 8,
  },
  score: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  section: {
    padding: 20,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  label: {
    fontSize: 14,
    color: '#666',
  },
  value: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});
