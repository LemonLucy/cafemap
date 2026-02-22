import React from 'react';
import {View, Text, StyleSheet, TouchableOpacity} from 'react-native';
import {Cafe, BlogAnalysis} from '../types';

interface Props {
  cafe: Cafe;
  analysis?: BlogAnalysis;
  onPress: () => void;
}

export const CafeListItem: React.FC<Props> = ({cafe, analysis, onPress}) => {
  const getSignalColor = (color: string) => {
    switch (color) {
      case 'green':
        return '#4CAF50';
      case 'yellow':
        return '#FFC107';
      case 'red':
        return '#F44336';
      default:
        return '#9E9E9E';
    }
  };

  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.header}>
        <View style={styles.titleRow}>
          {analysis && (
            <View
              style={[
                styles.signal,
                {backgroundColor: getSignalColor(analysis.signalColor)},
              ]}
            />
          )}
          <Text style={styles.name} numberOfLines={1}>
            {cafe.name}
          </Text>
        </View>
        {analysis && (
          <Text style={styles.score}>{analysis.totalScore.toFixed(1)}</Text>
        )}
      </View>

      <Text style={styles.address} numberOfLines={1}>
        {cafe.address}
      </Text>

      {cafe.distance !== undefined && (
        <Text style={styles.distance}>{cafe.distance}m</Text>
      )}

      {analysis && (
        <View style={styles.tags}>
          <Tag label={`작업 ${analysis.workScore}/10`} />
          <Tag label={analysis.outletLevel} />
          <Tag label={analysis.noiseLevel} />
          {analysis.hasWifi && <Tag label="WiFi" />}
        </View>
      )}
    </TouchableOpacity>
  );
};

const Tag: React.FC<{label: string}> = ({label}) => (
  <View style={styles.tag}>
    <Text style={styles.tagText}>{label}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  signal: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  score: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginLeft: 8,
  },
  address: {
    fontSize: 13,
    color: '#666',
    marginBottom: 4,
  },
  distance: {
    fontSize: 12,
    color: '#999',
    marginBottom: 8,
  },
  tags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  tag: {
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  tagText: {
    fontSize: 11,
    color: '#666',
  },
});
