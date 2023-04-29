const fs = require('fs');
const d3 = await import("d3");

main();



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

    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);

    const xAxis = d3.axisBottom(x);
    const yAxis = d3.axisLeft(y);

    const line = d3.line()
      .x(d => x(new Date(d.Timestamp)))
      .y(d => y(d.V1));

    const svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(d3.extent(labels, d => new Date(d)));
    y.domain([0, d3.max(v1Data, d => d)]);

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
      .attr("d", line);

  } catch (err) {
    console.log(err);
  }
});
