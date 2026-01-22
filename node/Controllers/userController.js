"use strict";

const firebase = require("../db");
const User = require("../Models/User");
const firestore = firebase.firestore();

const getUsers = async (req, res, next) => {
  try {
    const users = await firestore.collection("users");
    const data = await users.get();
    const usersList = [];

    if (data.empty) {
      res.status(404).send("No users found!");
    } else {
      data.forEach((doc) => {
        //fix the return model later
        const user = new User(
          doc.data().id,
          doc.data().accessToken,
          doc.data().displayName,
          doc.data().email,
          doc.data().photoURL,
          doc.data().isAdmin,
          doc.id
        );
        usersList.push(user);
      });
      res.status(200).send(usersList);
    }
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const getUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const data = await user.get();

    if (!data.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      res.status(200).send(data.data());
    }
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const updateUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    const data = req.body;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();

    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update(data);
      res.status(200).send("User updated successfully!");
    }
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const makeAdmin = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();
    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update({
        isAdmin: true,
      });

      const updated = await user.get();
      res.status(200).send(updated.data());
    }
  } catch (error) {
    console.log(error)
    res.status(400).send(error.message);
  }
};

const removeAdmin = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();
    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update({
        isAdmin: false,
      });

      const updated = await user.get();
      res.status(200).send(updated.data());
    }
  } catch (error) {
    console.log(error)
    res.status(400).send(error.message);
  }
};

const addUser = async (req, res, next) => {
  try {
    const data = req.body;

    if (!data || !data.id) {
      return res.status(400).send("User 'id' is required");
    }

    const docRef = firestore.collection("users").doc(String(data.id));
    const existing = await docRef.get();

    // Upsert: create if missing, otherwise merge updates
    if (existing.exists) {
      await docRef.set(data, { merge: true });
    } else {
      await docRef.set(data);
    }

    const saved = await docRef.get();
    res.status(201).send({
      message: existing.exists ? "User updated successfully!" : "User created successfully!",
      result: saved.data(),
    });
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const deleteUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    await firestore.collection("users").doc(id).delete();
    res.status(200).send("User deleted successfully!");
  } catch (error) {
    res.status(400).send(error.message);
  }
};

module.exports = {
  getUsers,
  getUser,
  updateUser,
  addUser,
  deleteUser,
  makeAdmin,
  removeAdmin,
};
