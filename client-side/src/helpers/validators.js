export const validatorPositive = (value) => {
  if (value >= 0) {
    return true;
  }
  return false;
};

export const validatorPassword = (password) => {
  /* eslint-disable no-useless-escape */
  const regExp = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*()]).{8,}/;
  /* eslint-enable no-useless-escape */
  const validPassword = regExp.test(password);
  return validPassword;
};

export const validatiorPassword = (val) => {
  const regExp =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d\D\W]{7,}(\w|\d)$/;
  return regExp.test(val);
};

export const validatorIntNumber = (val) => {
  if (val > 2147483647) {
    return false;
  }
  const regExp = /(^\d{1,10}$)/;
  return regExp.test(val);
};
