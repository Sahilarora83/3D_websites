// API Configuration file
// Use this in your components/pages

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const fetchImage = async (imagePath) => {
  const encodedUrl = encodeURIComponent(imagePath);
  const apiUrl = `${API_URL}/_next/image/?url=${encodedUrl}`;
  
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.statusText}`);
    }
    return response;
  } catch (error) {
    console.error('Image fetch error:', error);
    throw error;
  }
};

export default API_URL;
