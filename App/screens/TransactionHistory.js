import react, { useState } from "react";
import { View, Text, StyleSheet, FlatList } from "react-native";
import Mic from "../components/Mic.js";
import SearchBar from "../components/SearchBar.js";

const PaymentScreen = ({ navigation }) => {
  const [searchText, setSearchText] = useState("");
  return (
    <View style={styles.container}>
      <Text>TransactionHistory</Text>
    </View>
  );
};

export default PaymentScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
});
