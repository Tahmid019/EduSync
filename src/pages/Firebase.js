// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyA7vsQ6YgZsbcIT-xDNbmFkjM99RktqVBs",
    authDomain: "lipsync-f8097.firebaseapp.com",
    projectId: "lipsync-f8097",
    storageBucket: "lipsync-f8097.appspot.com",
    messagingSenderId: "10160932793",
    appId: "1:10160932793:web:8aabaf3b4e32ec61685868",
    measurementId: "G-QYVR6QJHH3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
export { db }