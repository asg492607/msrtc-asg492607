import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  StyleSheet, ActivityIndicator, Alert, KeyboardAvoidingView
} from 'react-native';
import { conductorApi } from '../../lib/api/client';
import { useAuthStore } from '../../store/useAuthStore';

export function LoginScreen({ navigation }: any) {
  const [employeeId, setEmployeeId] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState<1|2>(1);
  const [loading, setLoading] = useState(false);
  const login = useAuthStore(s => s.login);

  const handleSendOtp = async () => {
    if (!employeeId || !phone) { Alert.alert('Error', 'Enter Employee ID and Phone'); return; }
    setLoading(true);
    await conductorApi.auth.requestOtp(employeeId, phone);
    setLoading(false);
    setStep(2);
    Alert.alert('OTP Sent', 'Use 1234 for testing');
  };

  const handleVerify = async () => {
    setLoading(true);
    try {
      const conductor = await conductorApi.auth.verifyOtp(employeeId, otp);
      login(conductor);
    } catch (e: any) {
      Alert.alert('Error', e.message);
    }
    setLoading(false);
  };

  return (
    <KeyboardAvoidingView behavior="padding" style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>MSRTC</Text>
        <Text style={styles.subtitle}>Conductor Application</Text>
      </View>

      <View style={styles.card}>
        {step === 1 ? (
          <>
            <Text style={styles.label}>Employee ID</Text>
            <TextInput
              style={styles.input} value={employeeId}
              onChangeText={setEmployeeId} placeholder="e.g. EMP-1234"
              autoCapitalize="characters"
            />
            <Text style={styles.label}>Registered Phone</Text>
            <TextInput
              style={styles.input} value={phone}
              onChangeText={setPhone} placeholder="10-digit number"
              keyboardType="phone-pad" maxLength={10}
            />
            <TouchableOpacity style={styles.btn} onPress={handleSendOtp} disabled={loading}>
              {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Send OTP</Text>}
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.label}>Enter OTP</Text>
            <TextInput
              style={[styles.input, styles.otpInput]} value={otp}
              onChangeText={setOtp} placeholder="1234"
              keyboardType="number-pad" maxLength={6}
            />
            <TouchableOpacity style={styles.btn} onPress={handleVerify} disabled={loading}>
              {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Verify & Sign In</Text>}
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setStep(1)}>
              <Text style={styles.back}>← Change phone number</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0053A0', justifyContent: 'center', padding: 24 },
  header: { alignItems: 'center', marginBottom: 32 },
  logo: { fontSize: 36, fontWeight: '900', color: '#fff', letterSpacing: 2 },
  subtitle: { fontSize: 16, color: 'rgba(255,255,255,0.8)', marginTop: 4 },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 24, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 8, elevation: 5 },
  label: { fontSize: 14, color: '#555', marginBottom: 6, marginTop: 12, fontWeight: '600' },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, fontSize: 16, backgroundColor: '#fafafa' },
  otpInput: { textAlign: 'center', letterSpacing: 8, fontSize: 24, fontWeight: 'bold' },
  btn: { backgroundColor: '#0053A0', borderRadius: 8, padding: 14, alignItems: 'center', marginTop: 20 },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  back: { textAlign: 'center', color: '#0053A0', marginTop: 16, fontSize: 14 },
});
