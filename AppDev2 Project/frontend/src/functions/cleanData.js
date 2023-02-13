// step 1

function dataForGetSomeData(data) {
    const dataForChart = [];
    data.forEach((item) => {
        dataForChart.push({
            list_id: item.list_id,
            list_name: item.list_name,
            TotalCards: item.TotalCards,
            Completed: item.Completed,
            InProgress: item.InProgress,
            PastDeadline: item.PastDeadline
        });
    })
    return dataForChart;
}

export default dataForGetSomeData;