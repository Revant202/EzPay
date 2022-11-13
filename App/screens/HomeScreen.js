import { StyleSheet, Image, View, Text } from "react-native";

import Logo from "../Icons/Logo.svg";

import PrimaryButton from "../components/PrimaryButton";
import SecondaryButton from "../components/SecondaryButton";


export default function HomeScreen({ navigation }) {
function onClickHandler(){
    navigation.navigate("PaymentScreen")
}

  return (
    <View style={styles.container}>
      <View style={styles.view1}>
        <PrimaryButton onClick={onClickHandler}>Make Payment</PrimaryButton>
        <PrimaryButton>Check Balance</PrimaryButton>
        <PrimaryButton>Transaction History</PrimaryButton>
        <SecondaryButton>Add New Bank Account</SecondaryButton>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#2C734C",
  },
  view1: {
    flex: 1,
    margin: 50,
    padding: 50,
    justifyContent: "flex-start",
    alignItems: "center",
  },
});