// Custom image loader for Next.js
// Routes all image requests through ngrok backend

export default function imageLoader({ src, width, quality }) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  // Return direct path from ngrok server
  if (src.startsWith('http')) {
    // Already an absolute URL
    return src;
  }
  
  // Remove leading slash if present
  const imagePath = src.startsWith('/') ? src.slice(1) : src;
  
  // Return URL from ngrok server
  return `${apiUrl}/${imagePath}?w=${width}&q=${quality || 75}`;
}
