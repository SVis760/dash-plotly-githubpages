// assets/clientside.js
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = {
  updateDropdowns: function(vals, merged_df) {
    const maxLevel = 11;
    let outputs = [];

    for (let i = 2; i <= maxLevel; i++) {
      const valid = vals.slice(0, i - 1).every(val => val !== null && val !== undefined);

      if (!valid) {
        outputs.push([]); // Options for dropdown i
        outputs.push({ width: '100%', padding: '10px', display: 'none' }); // Hide dropdown i
      } else {
        // Make a deep copy of the data.
        let dfLocal = JSON.parse(JSON.stringify(merged_df));
        // Filter the data based on selections from previous dropdowns.
        for (let j = 1; j < i; j++) {
          dfLocal = dfLocal.filter(row => row[`prefLabelLaag${j}`] === vals[j - 1]);
        }
        // Get unique, sorted options for the current dropdown.
        const options = dfLocal
          .map(row => row[`prefLabelLaag${i}`])
          .filter((value, index, self) => self.indexOf(value) === index)
          .sort()
          .map(x => ({ label: x, value: x }));
        outputs.push(options);
        outputs.push({ width: '100%', padding: '10px', display: 'block' });
      }
    }
    return outputs;
  },

  updateDataTable: function(vals, merged_df) {
    let dfLocal = JSON.parse(JSON.stringify(merged_df));
    for (let i = 0; i < vals.length; i++) {
      if (vals[i] !== null && vals[i] !== undefined) {
        dfLocal = dfLocal.filter(row => row[`prefLabelLaag${i + 1}`] === vals[i]);
      }
    }
    return dfLocal;
  }
};
