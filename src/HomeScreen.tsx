import React from 'react';
import { View, ImageBackground, StyleSheet, Button } from 'react-native';

const HomeScreen = ({ navigation }) => {
    return (
        <ImageBackground 
            source={require('./assets/images/meditrack.jpg')} 
            style={styles.background}
        >
            <View style={styles.buttonContainer}>
                <Button 
                    title="Admin Login" 
                    onPress={() => navigation.navigate('AdminLogin')} 
                />
                <Button 
                    title="Doctor Login" 
                    onPress={() => navigation.navigate('DoctorLogin')} 
                />
                <Button 
                    title="Patient Login" 
                    onPress={() => navigation.navigate('PatientLogin')} 
                />
                <Button 
                    title="Sign Up" 
                    onPress={() => navigation.navigate('SignUp')} 
                />
            </View>
        </ImageBackground>
    );
};

const styles = StyleSheet.create({
    background: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    buttonContainer: {
        width: '80%',
        justifyContent: 'space-around',
        marginVertical: 20,
    },
});

export default HomeScreen;