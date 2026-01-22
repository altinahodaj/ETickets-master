class User {
  constructor(id, accessToken, displayName, email, photoURL, isAdmin) {
    this.id = id;
    this.accessToken = accessToken;
    this.displayName = displayName;
    this.email = email;
    this.photoURL = photoURL;
    this.isAdmin = isAdmin;
  }
}

module.exports = User;
