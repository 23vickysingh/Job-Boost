/**
 * Email validation utility functions
 */

/**
 * Validates email format using a comprehensive regex pattern
 * @param email - The email string to validate
 * @returns boolean - true if email is valid, false otherwise
 */
export const isValidEmail = (email: string): boolean => {
  // Comprehensive email regex pattern that covers most valid email formats
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  // Additional checks for edge cases
  if (!email || email.trim() === '') {
    return false;
  }
  
  // Check length limits (email should not exceed 254 characters)
  if (email.length > 254) {
    return false;
  }
  
  // Check if email contains consecutive dots
  if (email.includes('..')) {
    return false;
  }
  
  // Check if email starts or ends with a dot
  if (email.startsWith('.') || email.endsWith('.')) {
    return false;
  }
  
  return emailRegex.test(email.trim());
};

/**
 * Gets a user-friendly error message for invalid emails
 * @param email - The email string that was validated
 * @returns string - Error message describing the validation issue
 */
export const getEmailErrorMessage = (email: string): string => {
  if (!email || email.trim() === '') {
    return 'Email is required';
  }
  
  if (email.length > 254) {
    return 'Email is too long (maximum 254 characters)';
  }
  
  if (email.includes('..')) {
    return 'Email cannot contain consecutive dots';
  }
  
  if (email.startsWith('.') || email.endsWith('.')) {
    return 'Email cannot start or end with a dot';
  }
  
  if (!email.includes('@')) {
    return 'Email must contain @ symbol';
  }
  
  const parts = email.split('@');
  if (parts.length !== 2) {
    return 'Email must contain exactly one @ symbol';
  }
  
  const [localPart, domainPart] = parts;
  
  if (localPart.length === 0) {
    return 'Email must have content before @ symbol';
  }
  
  if (domainPart.length === 0) {
    return 'Email must have content after @ symbol';
  }
  
  if (!domainPart.includes('.')) {
    return 'Email domain must contain at least one dot';
  }
  
  return 'Please enter a valid email address';
};
