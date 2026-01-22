import firebase from "firebase/app";
import "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBwCfevIeO_qsbJZaeWpJKYQyDTEvLEkz8",
  authDomain: "e-tickets-1871d.firebaseapp.com",
  projectId: "e-tickets-1871d",
  storageBucket: "e-tickets-1871d.appspot.com",
  messagingSenderId: "293188362138",
  appId: "1:293188362138:web:3b37db09fac9f778d3e423",
  measurementId: "G-L9T73D4S0H"
};

const fireabaseApp = firebase.initializeApp(firebaseConfig);
const timestamp = firebase.firestore.FieldValue.serverTimestamp;

const getAuth = firebase.auth();
export { timestamp, getAuth };
export default fireabaseApp.firestore();