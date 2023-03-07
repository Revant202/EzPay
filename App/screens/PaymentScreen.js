import react, { useState } from "react";
import { View, Text, StyleSheet, FlatList } from "react-native";
import Mic from "../components/Mic.js";
import SearchBar from "../components/SearchBar.js";

const PaymentScreen = ({navigation,route}) => {
  const { search_name, search_amount } = route.params;
  const [name, setName] = useState(search_name);
  const [amount, setAmount] = useState(search_amount);
  console.log(search_amount + "ok")
  return (
    <View style={styles.container}>
      <SearchBar
        searchName={name}
        setSearchName={setName}
        searchAmount={amount}
        setSearchAmount={setAmount}
      />
      <Mic navigation={navigation} />
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
