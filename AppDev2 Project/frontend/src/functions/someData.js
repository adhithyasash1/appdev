// step 2

function dataForGraphData(cleanData) {
    let dict = [];
    // eslint-disable-next-line no-unused-vars
    for (let i = 0; i < cleanData.length; i++)
    {
        let y = {};
        y['list_id'] = cleanData[i].list_id;
        y['name'] = cleanData[i].list_name;
        y['xValues'] = ["TotalCards", "Completed", "In Progress", "Past Deadline"];
        y['yValues'] = [cleanData[i].TotalCards, cleanData[i].Completed, cleanData[i].InProgress, cleanData[i].PastDeadline];
        y['barColors'] = ['#41B883', '#E46651', '#00D8FF', '#DD1B16'];
        dict.push(y);
    }
    return dict;
}

export default dataForGraphData;