export const formatJsonToBullets = (jsonString) => {
  try {
    const jsonObj = JSON.parse(jsonString);
    return Object.entries(jsonObj).map(([key, value]) => {
      return `${key}: ${value}`;
    });
  } catch (error) {
    console.error('Invalid JSON string:', error);
    return [];
  }
};
