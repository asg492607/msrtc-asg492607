import { PassengerInput, ContactDetailsInput } from '../types';

export const validatePassenger = (p: PassengerInput): string | null => {
  if (!p.name || p.name.length < 3) return "Name must be at least 3 characters";
  const ageNum = parseInt(p.age, 10);
  if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) return "Age must be between 1 and 120";
  if (!p.gender) return "Please select a gender";
  return null;
};

export const validateContact = (c: ContactDetailsInput): string | null => {
  if (!c.mobile || c.mobile.length !== 10 || !/^\d+$/.test(c.mobile)) return "Mobile must be 10 digits";
  if (!c.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email)) return "Invalid email address";
  return null;
};
