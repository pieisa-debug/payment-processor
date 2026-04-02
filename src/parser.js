// parser.js
const fs = require('fs');
const path = require('path');

/**
 * Parses a file containing payment records.
 *
 * @param {string} filePath The path to the file.
 * @param {string} fileType The type of the file (e.g., 'csv', 'json').
 * @returns {Promise<Array<object>>} A promise that resolves to an array of payment record objects.
 * @throws {Error} If the file type is not supported or if there's an error during parsing.
 */
async function parseFile(filePath, fileType) {
  try {
    const fileContent = await fs.promises.readFile(filePath, 'utf-8');

    switch (fileType.toLowerCase()) {
      case 'csv':
        return parseCsv(fileContent);
      case 'json':
        return parseJson(fileContent);
      default:
        throw new Error(`Unsupported file type: ${fileType}`);
    }
  } catch (error) {
    console.error('Error parsing file:', error.message);
    throw error; // Re-throw the error to be handled upstream
  }
}

/**
 * Parses a CSV string into an array of payment record objects.
 * Assumes the first line is the header.
 *
 * @param {string} csvString The CSV string.
 * @returns {Array<object>} An array of payment record objects.
 */
function parseCsv(csvString) {
  const lines = csvString.trim().split('\n');
  if (lines.length < 2) {
    return []; // Return empty array if there's no data besides the header
  }

  const header = lines[0].split(',').map(header => header.trim());
  const data = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(value => value.trim());
    if (values.length !== header.length) {
      console.warn(`Skipping line ${i + 1} due to incorrect number of columns.`);
      continue; // Skip lines with incorrect columns
    }

    const record = {};
    for (let j = 0; j < header.length; j++) {
      record[header[j]] = values[j];
    }
    data.push(record);
  }

  return data;
}

/**
 * Parses a JSON string into an array of payment record objects.
 *
 * @param {string} jsonString The JSON string.
 * @returns {Array<object>} An array of payment record objects.
 * @throws {Error} If the JSON string is invalid.
 */
function parseJson(jsonString) {
  try {
    const jsonData = JSON.parse(jsonString);
    if (!Array.isArray(jsonData)) {
      throw new Error('JSON data must be an array of objects.');
    }
    return jsonData;
  } catch (error) {
    console.error('Error parsing JSON:', error.message);
    throw error; // Re-throw the error to be handled upstream
  }
}

module.exports = {
  parseFile,
};