import { View, TextInput,StyleSheet } from "react-native";
import React from "react";

const SearchBar = (props) => {
  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        value={props.searchText}
        onChangeText={(text) => props.setSearchText(text)}
        onSubmitEditing={props.onSubmit}
        placeholder={props.placeholder}
        keyboardType={props.type}
      />
    </View>
  );
};

export default SearchBar;

const styles = StyleSheet.create({
  container: {
    margin: 10,
  },
  input: {
    backgroundColor: "#fff",
    padding: 10,
    borderRadius: 10,
    color: "#000",
    borderWidth: 1,
  },
});
