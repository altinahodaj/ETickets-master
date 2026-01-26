import firebase from "firebase/compat/app";
import "firebase/compat/firestore";
import "firebase/compat/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBmSyq7Y-QEkF1c5MxEdIhdf2p0a_yiltY",
  authDomain: "e-tickets-1871d-2cb76.firebaseapp.com",
  projectId: "e-tickets-1871d-2cb76",
  storageBucket: "e-tickets-1871d-2cb76.firebasestorage.app",
  messagingSenderId: "911479925220",
  appId: "1:911479925220:web:4b3e8ea1681eec68f4bff1",
  measurementId: "G-E7RMVVM81L"
};

const fireabaseApp = !firebase.apps.length ? firebase.initializeApp(firebaseConfig) : firebase.app();
const timestamp = firebase.firestore.FieldValue.serverTimestamp;

const getAuth = firebase.auth();
export { timestamp, getAuth };
export default fireabaseApp.firestore();