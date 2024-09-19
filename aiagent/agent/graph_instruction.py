
barGraphIntstruction = '''

Where data is: {
  data: [
    {'name': string, 'value1': string | number}, 
    {'name': string, 'value1': string | number}, 
    {'name': string, 'value1': string | number},
    ...
    ],
  name: string, // this key represents the meaning of the 'name' key in data array
  value1: string // this key represents the meaning of the 'value1' key in data array
  value1?: string // this key represents the meaning of the 'value2' key in data array etc
  ...
}

// Examples of usage:
Each item in data array represents a different entity. 
The value fields, (value1, value2..) represents columns on the x axis.
Think of as attributes of that entity.

Here we are looking at average income for each month.
1. {
    data: [
      {name: 'Jan', value1: 20}, 
      {name: 'Feb', value1: 30}, 
      {name: 'Mar', value1: 40}, 
      {name: 'Apr', value1: 10},
      {name: 'May', value1: 45},
      {name: 'Jun', value1: 10},
      {name: 'Jul', value1: 80}, 
      {name: 'Aug', value1: 10},
      {name: 'Sept',value1: 60}, 
      {name: 'Oct', value1: 10},
      {name: 'Nov', value1: 60}, 
      {name: 'Dec', value1: 10},
    ],
    name: "Month",  // this to indicate that the "name" field in data represents the month entity
    value1: "Average_Income", // this to indicate that the 'value1' field in data item represents the attribute Average_Income of that  entity
}

Here we are looking at average income, and average spends for each month.
Since there are two attributes for each entity, we have two items in values(value1, value2).
2. {
    data: [
      {name: 'Jan', value1: 20,  value2: 40}, 
      {name: 'Feb': value1: 30,  value2: 50}, 
      {name: 'Mar': value1: 40,  value2: 5}, 
      {name: 'Apr', value1: 10,  value2: 10},
      {name: 'May', value1: 45,  value2: 15}, 
      {name: 'Jun', value1: 10,  value2: 55},
      {name: 'Jul', value1: 80,  value2: 20}, 
      {name: 'Aug', value1: 10,  value2: 25},
      {name: 'Sept',value1: 60,  value2: 70}, 
      {name: 'Oct', value1: 10,  value2: 3},
      {name: 'Nov', value1: 60,  value2: 4.5}, 
      {name: 'Dec', value1: 10,  value2: 8},
    ],
    name: "Month", // this to indicate that the "name" field in data represents the month entity
    value1: "Average_Income", // this to indicate that the 'value1' field in data item represents the attribute Average_Income of that  entity
    value2: "Average_Spends" // this to indicate that the 'value2' field in data item represents the attribute Average_Spends of that  entity
}

Here we are looking at the performance of american and european players for each series. 
Since there are two attributes for each entity, we have two items in values(value1, value2).
3.  {
      data: [
        { name: 'series A', value1: 10, value2: 40}, 
        { name: 'series B', value1: 45, value2: 70}
      ],
      name: 'Series', // this to indicate that the "name" field in data represents the series value
      value1: 'American', // this to indicate that the 'value1' field in data represents the nationality American
      value2: 'European' // similarly, 'value2' key here indicates that the 'value2' field in data represents nationality European
    }

4. Here we're looking at average spends over swiggy and zomato for each month
Since there are two attributes for each entity, we have two items in values(value1, value2).
2. {
    data: [
      {name: 'Jan', value1: 20,  value2: 40}, 
      {name: 'Feb': value1: 30,  value2: 50}, 
      {name: 'Mar': value1: 40,  value2: 5}, 
      {name: 'Apr', value1: 10,  value2: 10},
      {name: 'May', value1: 45,  value2: 15}, 
      {name: 'Jun', value1: 10,  value2: 55},
      {name: 'Jul', value1: 80,  value2: 20}, 
      {name: 'Aug', value1: 10,  value2: 25},
      {name: 'Sept',value1: 60,  value2: 70}, 
      {name: 'Oct', value1: 10,  value2: 3},
      {name: 'Nov', value1: 60,  value2: 4.5}, 
      {name: 'Dec', value1: 10,  value2: 8},
    ],
    name: "Month", // this to indicate that the "name" field in data represents the month entity
    value1: "Swiggy_Average_Spends", // this to indicate that the 'value1' field in data item represents the attribute Swiggy's Average Spends of that entity
    value2: "Zomato_Average_Spends" // this to indicate that the 'value2' field in data item represents the attribute Zomato's Average Spends of that  entity
}


'''

horizontalBarGraphIntstruction = '''

Where data is: {
  data: [
    {'name': string, 'value1': string | number}, 
    {'name': string, 'value1': string | number}, 
    {'name': string, 'value1': string | number},
    ...
    ],
  name: string, // this key represents the meaning of the 'name' key in data array
  value1: string // this key represents the meaning of the 'value1' key in data array
  value1?: string // this key represents the meaning of the 'value2' key in data array etc
  ...
}

// Examples of usage:
Each item in data array represents a different entity. 
The value fields, (value1, value2..) represents columns on the x axis.
Think of as attributes of that entity.

Here we are looking at average income for each month.
1. {
    data: [
      {name: 'Jan', value1: 20}, 
      {name: 'Feb', value1: 30}, 
      {name: 'Mar', value1: 40}, 
      {name: 'Apr', value1: 10},
      {name: 'May', value1: 45},
      {name: 'Jun', value1: 10},
      {name: 'Jul', value1: 80}, 
      {name: 'Aug', value1: 10},
      {name: 'Sept',value1: 60}, 
      {name: 'Oct', value1: 10},
      {name: 'Nov', value1: 60}, 
      {name: 'Dec', value1: 10},
    ],
    name: "Month",  // this to indicate that the "name" field in data represents the month entity
    value1: "Average_Income", // this to indicate that the 'value1' field in data item represents the attribute Average_Income of that  entity
}

Here we are looking at average income, and average spends for each month.
Since there are two attributes for each entity, we have two items in values(value1, value2).
2. {
    data: [
      {name: 'Jan', value1: 20,  value2: 40}, 
      {name: 'Feb': value1: 30,  value2: 50}, 
      {name: 'Mar': value1: 40,  value2: 5}, 
      {name: 'Apr', value1: 10,  value2: 10},
      {name: 'May', value1: 45,  value2: 15}, 
      {name: 'Jun', value1: 10,  value2: 55},
      {name: 'Jul', value1: 80,  value2: 20}, 
      {name: 'Aug', value1: 10,  value2: 25},
      {name: 'Sept',value1: 60,  value2: 70}, 
      {name: 'Oct', value1: 10,  value2: 3},
      {name: 'Nov', value1: 60,  value2: 4.5}, 
      {name: 'Dec', value1: 10,  value2: 8},
    ],
    name: "Month", // this to indicate that the "name" field in data represents the month entity
    value1: "Average_Income", // this to indicate that the 'value1' field in data item represents the attribute Average_Income of that  entity
    value2: "Average_Spends" // this to indicate that the 'value2' field in data item represents the attribute Average_Spends of that  entity
}

Here we are looking at the performance of american and european players for each series. 
Since there are two attributes for each entity, we have two items in values(value1, value2).
2.  {
      data: [
        { name: 'series A', value1: 10, value2: 40}, 
        { name: 'series B', value1: 45, value2: 70}
      ],
      name: 'Series', // this to indicate that the "name" field in data represents the series value
      value1: 'American', // this to indicate that the 'value1' field in data represents the nationality American
      value2: 'European' // similarly, 'value2' key here indicates that the 'value2' field in data represents nationality European
    }


'''


lineGraphIntstruction = '''

Where data is: {
  data: [{'name': string, 'value1': string | number}, {'name': string, 'value1': string | number}, {'name': string, 'value1': string | number}],
  name: string, // this key represents the meaning of the 'name' key in data array
  value1: string // this key represents the meaning of the 'value1' key in data array
}

// Examples of usage:

Here we are looking at the average closing balance for each month.
1. {
  data: [{ name: "20-07-2023", value1: 530}, {name: "20-08-2023", value1: 700}, {name: "20-09-2023", value1: 300}, ..],
  name: "month", // this to indicate that the "name" field in data array represents the month value
  value1: 'Closing_Balance', // this to indicate that the 'value1' field in data represents the closing balance for that month.

}

Here we are looking at the performance of american and european players for each year. 
Since there are two entities, we have two value fields in the data array, value1 and value2 respectively
2.  {
      data: [{ name: '2020', value1: 2, value2: 2}, {{ name: '2021', value1: 5, value2: 7}}],
      name: 'year', // this to indicate that the "name" field in data represents the year value
      value1: 'American', // this to indicate that the 'value1' field in data represents the nationality American
      value2: 'European' // similarly, 'value2' key here indicates that the 'value2' field in data represents nationality European
    }
'''

pieChartIntstruction = '''

  Where data is: 
  {
    data: {
      pie_chart_1:{
        data: [
          { name: string, value: number | string },
          { name: string, value: number | string },
          { name: string, value: number | string },
          { name: string, value: number | string },
          ...
        ],
        label: string
    },
    pie_chart_2?:{
        data: [
          { name: string, value: number | string },
          { name: string, value: number | string },
          { name: string, value: number | string },
          { name: string, value: number | string },
          ...
        ],
        label: string
    }
    }
  }

// Example usage:
1. Here we are looking at transactions categorised by mode of payment.
{
  data: {
    pie_chart_1: {
      data: [
        { name: 'Mode A', value: 400 },
        { name: 'Mode B', value: 300 },
        { name: 'Mode C', value: 300 },
        { name: 'Mode D', value: 200 }, 
        ...
      ],
      label: "Transaction categorised by mode of payment"
    }
  }
}

2. Here we are looking at all the transactions categorised by transaction size, Large( > 10000 ), Medium( 2000 - 10000), and Small( < 2000)
{
  data: {
    pie_chart_1: {
      data: [
        { name: 'Large', value: 10 },
        { name: 'Medium', value: 40 },
        { name: 'Small', value: 50 }
      ],
      label: "Transactions categorised by transaction size"
    }
  }
}


3. Here we are looking at all the debit and credit transactions categorised by transaction size, Large( > 10000 ), Medium( 2000 - 10000), and Small( < 2000)
Here we see two separate pie charts, one for debit, and one for credit
{
  data: {
    pie_chart_1: {
      data: [
        { name: 'Large', value: 10 },
        { name: 'Medium', value: 40 },
        { name: 'Small', value: 50 }
      ],
      label: "Debit Transactions categorised by transaction size"
    },
    pie_chart_2: {
      data: [
        { name: 'Large', value: 1 },
        { name: 'Medium', value: 2 },
        { name: 'Small', value: 4 }
      ],
      label: "Credit Transactions categorised by transaction size"    
    }
  }
}


'''

scatterPlotIntstruction = '''
Where data is: {
  series: {
    data: { x: number; y: number; id: number }[]
    label: string
  }[]
}

// Examples of usage:
1. Here each data array represents the points for a different entity. 
We are looking for correlation between amount spent and quantity bought for men and women.
data = {
  series: [
    {
      data: [
        { x: 100, y: 200, id: 1 },
        { x: 120, y: 100, id: 2 },
        { x: 170, y: 300, id: 3 },
      ],
      label: 'Men',
    },
    {
      data: [
        { x: 300, y: 300, id: 1 },
        { x: 400, y: 500, id: 2 },
        { x: 200, y: 700, id: 3 },
      ],
      label: 'Women',
    }
  ],
}

2. Here we are looking for correlation between the height and weight of players.
data = {
  series: [
    {
      data: [
        { x: 180, y: 80, id: 1 },
        { x: 170, y: 70, id: 2 },
        { x: 160, y: 60, id: 3 },
      ],
      label: 'Players',
    },
  ],
}

// Note: Each object in the 'data' array represents a point on the scatter plot.
// The 'x' and 'y' values determine the position of the point, and 'id' is a unique identifier.
// Multiple series can be represented, each as an object in the outer array.
'''

tableInstruction = '''
where data is: {
  data: [
    { key1: string| number,  key2: string| number,  key3: string| number, key4: string| number, key5: string| number, ... },
    { key1: string| number,  key2: string| number,  key3: string| number, key4: string| number, key5: string| number, ... },
    { key1: string| number,  key2: string| number,  key3: string| number, key4: string| number, key5: string| number, ... },
  ]
}
Ensure that the output is an array of objects, where each object represents a row in the table.

Example.
1. Here we are looking to list all the transactions.
{
  data: [
    { transaction_name: "1",  transaction_amount: 400,  transaction_date: "20/4/2023", transaction_type: debit, ... },
    { transaction_name: "abc",  transaction_amount: 400.4,  transaction_date: "22/4/2023", transaction_type: credit, ... },
    { transaction_name: "ewe",  transaction_amount: 20,  transaction_date: "20/5/2023", transaction_type: debit, ... },
  ]
}
'''

graph_instructions = {
    "bar": barGraphIntstruction,
    "horizontalBar": horizontalBarGraphIntstruction,
    "line": lineGraphIntstruction,
    "pie": pieChartIntstruction,
    "scatter": scatterPlotIntstruction,
    "table": tableInstruction
}