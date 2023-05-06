import fs from 'fs'
import {scaleTime, scaleLinear, axisBottom, axisLeft, line, select, extent, max} from 'd3'

// const fs = require('fs');
// const d3 = require("d3");

// main();



fs.readFile("./data.json", (err, jsonString) => {
  if (err) {
    console.log("Error reading file from disk:", err);
    return;
  }
  try {
    const data = JSON.parse(jsonString);
    const readings = data.logs[data.logs.length - 1].Readings;
    const labels = readings.map(reading => reading.Timestamp);
    const v1Data = readings.map(reading => reading.V1);

    const margin = { top: 20, right: 20, bottom: 30, left: 50 };
    const width = 960 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const x = scaleTime().range([0, width]);
    const y = scaleLinear().range([height, 0]);

    const xAxis = axisBottom(x);
    const yAxis = axisLeft(y);

    var l = line()
      .x(d => x(new Date(d.Timestamp)))
      .y(d => y(d.V1));

    const svg = select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(extent(labels, d => new Date(d)));
    y.domain([0, max(v1Data, d => d)]);

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .call(yAxis)
      .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Voltage");

    svg.append("path")
      .datum(readings)
      .attr("class", "line")
      .attr("d", l);

  } catch (err) {
    console.log(err);
  }
});
