import React, { useEffect, useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ActivityIndicator, FlatList, SafeAreaView, Platform, TouchableOpacity, Linking } from 'react-native';

// Important: Ensure this matches your running ngrok URL
const API_URL = 'https://edition-valley-engaging.ngrok-free.dev/api/dashboard/9876543210';

const formatTimestamp = (ms: number) => {
  if (!ms) return 'Just now';
  const date = new Date(ms);
  return date.toLocaleString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: true
  });
};

export default function App() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = () => {
      fetch(API_URL, {
        headers: {
          'ngrok-skip-browser-warning': 'true'
        }
      })
        .then(res => res.json())
        .then(json => {
          setData(json);
          setLoading(false);
        })
        .catch(err => {
          console.error("Error fetching dashboard:", err);
          setLoading(false);
        });
    };

    fetchDashboard(); // initial load
    const interval = setInterval(fetchDashboard, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const handleCallVaaniPay = () => {
    Linking.openURL('tel:+16626645364');
  };

  if (loading && !data) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#0A2463" />
        <Text style={{ marginTop: 10, color: '#0A2463', fontWeight: 'bold' }}>Loading VaaniPay...</Text>
      </View>
    );
  }

  if (!data || data.error) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>Failed to connect to secure bank server.</Text>
      </View>
    );
  }

  const renderTransaction = ({ item }: { item: any }) => {
    const isDebit = item.type.toLowerCase() === 'debit';
    return (
      <View style={styles.txnCard}>
        <View style={styles.txnLeft}>
          <View style={[styles.txnIconContainer, isDebit ? styles.iconDebit : styles.iconCredit]}>
            <Text style={styles.txnIconText}>{isDebit ? '↑' : '↓'}</Text>
          </View>
          <View style={styles.txnDetails}>
            <Text style={styles.txnDesc}>{item.desc}</Text>
            <Text style={styles.txnDate}>{formatTimestamp(item.timestamp)}</Text>
          </View>
        </View>
        <Text style={[styles.txnAmount, isDebit ? styles.textDebit : styles.textCredit]}>
          {isDebit ? '-' : '+'}₹{item.amount.toLocaleString('en-IN')}
        </Text>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header Background */}
      <View style={styles.headerBackground}>
        <Text style={styles.headerGreeting}>Good evening, {data.user.name.split(' ')[0]}</Text>
        <Text style={styles.headerSubtitle}>VaaniPay Secure Banking</Text>
      </View>

      {/* Main Balance Card */}
      <View style={styles.balanceCard}>
        <Text style={styles.cardLabel}>Available Balance</Text>
        <Text style={styles.balanceText}>₹{data.account.balance.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</Text>
        
        <View style={styles.scoreRow}>
          <Text style={styles.scoreLabel}>VaaniPay Credit Score:</Text>
          <Text style={styles.scoreValue}>{data.credit_score} / 900</Text>
        </View>

        <View style={styles.divider} />

        {/* Action Buttons */}
        <View style={styles.actionRow}>
          <TouchableOpacity style={styles.actionButton} onPress={handleCallVaaniPay}>
            <View style={[styles.actionIcon, { backgroundColor: '#E3F2FD' }]}>
              <Text style={{ fontSize: 20 }}>📞</Text>
            </View>
            <Text style={styles.actionText}>Call AI</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton}>
            <View style={[styles.actionIcon, { backgroundColor: '#E8F5E9' }]}>
              <Text style={{ fontSize: 20 }}>💸</Text>
            </View>
            <Text style={styles.actionText}>Transfer</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton}>
            <View style={[styles.actionIcon, { backgroundColor: '#FFF3E0' }]}>
              <Text style={{ fontSize: 20 }}>📱</Text>
            </View>
            <Text style={styles.actionText}>Scan QR</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Transactions Section */}
      <View style={styles.transactionsHeader}>
        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <TouchableOpacity><Text style={styles.seeAllText}>See all</Text></TouchableOpacity>
      </View>

      <FlatList
        data={data.transactions}
        keyExtractor={(item, index) => item.id || index.toString()}
        renderItem={renderTransaction}
        contentContainerStyle={{ paddingHorizontal: 20, paddingBottom: 40 }}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={<Text style={styles.emptyText}>No recent transactions.</Text>}
      />

      <StatusBar style="light" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F7F9FC',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F7F9FC',
  },
  headerBackground: {
    backgroundColor: '#0A2463', // Deep premium blue
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 80,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerGreeting: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    color: '#8CA0CB',
    fontSize: 14,
    marginTop: 4,
  },
  balanceCard: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    marginTop: -50, // Float over header
    borderRadius: 20,
    padding: 24,
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 15,
    shadowOffset: { width: 0, height: 8 },
    elevation: 8,
  },
  cardLabel: {
    fontSize: 14,
    color: '#64748B',
    fontWeight: '500',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  balanceText: {
    fontSize: 38,
    fontWeight: '800',
    color: '#0F172A',
    marginVertical: 10,
  },
  scoreRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 5,
  },
  scoreLabel: {
    fontSize: 14,
    color: '#64748B',
  },
  scoreValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#059669', // Emerald green
  },
  divider: {
    height: 1,
    backgroundColor: '#F1F5F9',
    marginVertical: 20,
  },
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
  },
  actionButton: {
    alignItems: 'center',
  },
  actionIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  actionText: {
    fontSize: 13,
    color: '#475569',
    fontWeight: '500',
  },
  transactionsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 25,
    marginTop: 25,
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#0F172A',
  },
  seeAllText: {
    fontSize: 14,
    color: '#2563EB',
    fontWeight: '600',
  },
  txnCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.03,
    shadowRadius: 5,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  txnLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  txnIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  iconDebit: {
    backgroundColor: '#FEE2E2', // Light red
  },
  iconCredit: {
    backgroundColor: '#D1FAE5', // Light green
  },
  txnIconText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  txnDetails: {
    justifyContent: 'center',
  },
  txnDesc: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1E293B',
    marginBottom: 4,
  },
  txnDate: {
    fontSize: 12,
    color: '#94A3B8',
  },
  txnAmount: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  textDebit: {
    color: '#DC2626', // Red
  },
  textCredit: {
    color: '#059669', // Green
  },
  errorText: {
    color: '#DC2626',
    textAlign: 'center',
    padding: 20,
    fontSize: 16,
    fontWeight: '500',
  },
  emptyText: {
    textAlign: 'center',
    color: '#94A3B8',
    marginTop: 30,
    fontSize: 15,
  }
});
