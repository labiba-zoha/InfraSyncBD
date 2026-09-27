import mysql from 'mysql2/promise';

async function checkDb() {
  const connection = await mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'infrasync_bd'
  });
  
  try {
    const [columns] = await connection.query('SHOW COLUMNS FROM complaints');
    console.log(columns.map(c => c.Field));
  } catch (e) {
    console.error(e);
  } finally {
    await connection.end();
  }
}
checkDb();
