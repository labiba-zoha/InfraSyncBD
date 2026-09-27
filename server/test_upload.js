import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';

// Create a dummy image file
const dummyImagePath = path.join(process.cwd(), 'dummy.png');
fs.writeFileSync(dummyImagePath, 'fake image content');

const token = jwt.sign({ userId: 1, role: 'contractor' }, 'infrasync_secret_key_2026');

async function testUpload() {
  const formData = new FormData();
  formData.append('status', 'Under Review');
  formData.append('resolutionSummary', 'Fixed the pothole properly');
  
  // Use node fetch to send multipart
  const blob = new Blob([fs.readFileSync(dummyImagePath)], { type: 'image/png' });
  formData.append('photo', blob, 'dummy.png');

  try {
    // Assuming there is a complaint with ID 'CMP-80002' which exists according to screenshot
    const response = await fetch('http://localhost:5000/api/complaints/CMP-80002/status', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    const result = await response.json();
    console.log('Upload Result:', result);
    
    // Fetch complaints to verify
    const getResponse = await fetch('http://localhost:5000/api/complaints', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const { data } = await getResponse.json();
    const updated = data.find(c => c.complaint_ticket_no === 'CMP-80002');
    console.log('Updated Complaint in DB:', {
      status: updated.status,
      resolution_summary: updated.resolution_summary,
      resolution_photo_url: updated.resolution_photo_url
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

testUpload();
