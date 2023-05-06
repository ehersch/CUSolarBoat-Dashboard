import fs from 'fs';
import * as d3 from 'd3';
import puppeteer from 'puppeteer';

// Read the JSON file
const data = JSON.parse(fs.readFileSync('/Users/tasmin/Documents/GitHub/2122CUSBSyscoRepo/Dashboard/data.json'));

// Extract voltage readings from JSON
const readings = data.logs[data.logs.length - 1].Readings;
const labels = readings.map(reading => reading.Timestamp);
const v1Data = readings.map(reading => reading.V1);

// Create the SVG element
const width = 500;
const height = 300;
const margin = { top: 20, right: 20, bottom: 30, left: 50 };


(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('/Users/tasmin/Documents/GitHub/2122CUSBSyscoRepo/Dashboard/index.html');

  const svg = d3.select('body')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // Define the scales
  const x = d3.scaleBand()
    .range([0, width])
    .domain(data.map(d => d.name))
    .padding(0.1);

  const y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, d3.max(data, d => d.value)]);

  // Draw the bars
  svg.selectAll('.bar')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.name))
    .attr('y', d => y(d.value))
    .attr('width', x.bandwidth())
    .attr('height', d => height - y(d.value));

  // Draw the x-axis
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x));

  // Draw the y-axis
  svg.append('g')
    .call(d3.axisLeft(y));

  await browser.close();
})();





