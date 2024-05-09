import * as React from 'react';
import { useState, useEffect, useContext } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

import Row from './Row';
import UserContext from '../../contexts/UserContext';
import AddressContext from '../../contexts/AddressContext';
import PopCardSubmit from './PopCardSubmit';
import LoadingTable from './LoadingTable';

export default function VotingForm() {
  const [tableData, setTableData] = useState([]);
  const [allData, setAllData] = useState({});
  const [newMaxBudget, setNewMaxBudget] = useState(0);
  const [display, setDisplay] = useState(true);
  const maxBudget = 596770415000;

  const id = useContext(UserContext || JSON.stringify(localStorage.getItem('id')));
  const address = useContext(AddressContext);
  const url = `${address}voting?user_id=${id}`;


  // Receiving the budget table from the server
  const fetchData = async () => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const information = await response.json();
      setAllData(information);
      setTableData(information.children);
    } catch (error) {
      console.error(error);
    }
    return {};
  };

  useEffect(() => {
    fetchData(); // fetch data asynchronously
  }, []);

  // Finding a path from the root to a specific node
  const findPathById = (idToFind, data, path = []) => {
    for (let i = 0; i < data.length; i += 1) {
      if (data[i].id === idToFind) {
        return path;
      }
      if (data[i].children.length > 0) {
        const childResult = findPathById(idToFind, data[i].children, [...path, data[i].id]);
        if (childResult) {
          return childResult;
        }
      }
    }
    return null;
  };

  // Clears all clicks on the checkboxes
  const clearAll = () => {
    const tableClear = clear(tableData);
    setTableData(tableClear);
  };

  // Helper function that clears all clicks on the checkboxes
  const clear = (data) => {
    const clearData = data.map((row) => {
      if (row.children.length > 0) {
        return { ...row, checked: false, children: clear(row.children) };
      }
      return { ...row, checked: false };
    });
    return clearData;
  };

  // A function that calculates the total budget for all the rows that are not checked
  const TotalBudget = (data) => {
    const newTotalBudget = data.reduce((total, item) => {
      if (item.checked) {
        return total;
      }
      return total + Number(item.allocated_budget_amount);
    }, 0);
    setNewMaxBudget(newTotalBudget);
    return newTotalBudget;
  };

  useEffect(() => {
    TotalBudget(tableData);
  }, [tableData]);

  // A function that changes the status of the checkbox from the root to the same node
  const handleCheckBox = (data, id, status) => {
    const updatedTable = data.map((row) => {
      if (row.id === id) {
        if (row.children.length > 0) {
          return { ...row, checked: status, children: helperHandleCheck(row.children, status) };
        }
        return { ...row, checked: status };
      }
      return { ...row };
    });

    const path = findPathById(id, tableData);
    if (path.length === 0) {
      setTableData(updatedTable);
    } else {
      const allTableData = tableData.map((row) => {
        if (row.id === path[0]) {
          return recHandleParentTrue(row, path.slice(1), updatedTable);
        }
        return { ...row };
      });
      setTableData(allTableData);
    }
  };

  const recHandleParentTrue = (data, path, updateTableData) => {
    if (path.length === 0) {
      return { ...data, checked: true, children: updateTableData };
    }
    const newData = data.children.map((row) => {
      if (row.id === path[0]) {
        return recHandleParentTrue(row, path.slice(1), updateTableData);
      }
      return { ...row };
    });
    return { ...data, checked: true, children: newData };
  };

  // Makes the status of the children to be the same as the parent's in the checkbox
  const helperHandleCheck = (table, status) =>
    table.map((row) =>
      row.children.length > 0
        ? { ...row, checked: status, children: helperHandleCheck(row.children, status) }
        : { ...row, checked: status }
    );

  const recHandle = (data, path, updateTableData) => {
    if (path.length === 0) {
      return { ...data, children: updateTableData };
    }
    const newData = data.children.map((row) => {
      if (row.id === path[0]) {
        return recHandle(row, path.slice(1), updateTableData);
      }
      return { ...row };
    });
    return { ...data, children: newData };
  };

  // Updates the budget of the Kid's and siblings of the node that was clicked
  const handleVote = (data, id, value, diff) => {
    // Update siblings/childs1 budget
    const maxBudget = TotalBudget(data);
    let updatedTableData = updateBudget(data, id, value, diff, maxBudget, 0);

    // Update childs2 budget
    updatedTableData = handleChildBudget(updatedTableData, id, value);

    // Update childs3 budget
    updatedTableData = updatedTableData.map((row) => {
      if (row.children.length > 0) {
        return { ...row, children: handleChildBudget(row.children, id, value) };
      }
      return { ...row };
    });

    // Update childs4 budget
    updatedTableData = updatedTableData.map((row) => {
      if (row.children.length > 0) {
        const children3 = row.children.map((child3) => {
          if (child3.children) {
            return { ...child3, children: handleChildBudget(child3.children, id, value) };
          }
          return { ...child3 };
        });
        return { ...row, children: children3 };
      }
      return { ...row };
    });

    // Update childs5 budget
    updatedTableData = updatedTableData.map((row) => {
      if (row.children.length > 0) {
        const children3 = row.children.map((child3) => {
          if (child3.children.length > 0) {
            const children4 = child3.children.map((child4) => {
              if (child4.children.length > 0) {
                return { ...child4, children: handleChildBudget(child4.children, id, value) };
              }
              return { ...child4 };
            });
            return { ...child3, children: children4 };
          }
          return { ...child3 };
        });
        return { ...row, children: children3 };
      }
      return { ...row };
    });

    // Update childs6 budget
    updatedTableData = updatedTableData.map((row) => {
      if (row.children.length > 0) {
        const children3 = row.children.map((child3) => {
          if (child3.children.length > 0) {
            const children4 = child3.children.map((child4) => {
              if (child4.children.length > 0) {
                const children5 = child4.children.map((child5) => {
                  if (child5.children.length > 0) {
                    return { ...child5, children: handleChildBudget(child5.children, id, value) };
                  }
                  return { ...child5 };
                });
                return { ...child4, children: children5 };
              }
              return { ...child4 };
            });
            return { ...child3, children: children4 };
          }
          return { ...child3 };
        });
        return { ...row, children: children3 };
      }
      return { ...row };
    });

    const path = findPathById(id, tableData);
    if (path.length === 0) {
      setTableData(updatedTableData);
    } else {
      const allTableData = tableData.map((row) => {
        if (row.id === path[0]) {
          return recHandle(row, path.slice(1), updatedTableData);
        }
        return { ...row };
      });
      setTableData(allTableData);
    }
  };

  // An helper function that updates the children's budget
  const handleChildBudget = (data, id, value) => {
    const updatedTableData = data.map((row) => {
      if (row.children.length === 0) {
        return { ...row };
      }
      const totalChildBudget = row.children.reduce((total, item) => total + Number(item.allocated_budget_amount), 0);
      const budgetDiff = row.allocated_budget_amount - totalChildBudget;
      const childrens = updateBudget(row.children, id, value, budgetDiff, row.allocated_budget_amount, 1);
      return { ...row, children: childrens };
    });
    return updatedTableData;
  };

  // An helper function that updates the siblings budget
  const updateBudget = (data, id, value, diff, currMaxBudget, isChilds) => {
    let updatedTableData = data.slice(); // create a copy of tableData
    let countRows = isChilds ? data.length : data.length - 1; // count of rows to update

    const downRows = data.filter((row) => row.checked);
    countRows -= downRows.length;
    const checkedRows = data.filter((row) => !row.checked);
    const rowsIds = checkedRows.map((row) => row.id);
    let times = 1; // limit the while loop (not to stuck in inifinte loop)

    while (diff !== 0 && times < 20 && countRows > 0) {
      times += 1;
      let removedRows = 0; // count of rows that has reached to their max/0
      let remain = 0; // remaining difference to distribute among rows
      const budgetPerRow = diff / countRows;
      updatedTableData = updatedTableData.map((row) => {
        if (row.checked) {
          return { ...row };
        }
        if (isChilds === 0 && row.id === id) {
          if (value > currMaxBudget) {
            return { ...row, allocated_budget_amount: currMaxBudget };
          }
          return { ...row, allocated_budget_amount: value };
        }
        if (!rowsIds.includes(row.id)) {
          return { ...row };
        }
        let currBudget = parseFloat(row.allocated_budget_amount) + budgetPerRow;
        if (currBudget > currMaxBudget) {
          remain += currBudget - currMaxBudget;
          removedRows += 1;
          const indexToRemove = rowsIds.indexOf(row.id);
          rowsIds.splice(indexToRemove, 1);
          currBudget = currMaxBudget;
        }
        if (currBudget < 0) {
          remain += currBudget;
          removedRows += 1;
          const indexToRemove = rowsIds.indexOf(row.id);
          rowsIds.splice(indexToRemove, 1);
          currBudget = 0;
        }
        return { ...row, allocated_budget_amount: currBudget };
      });
      diff = remain;
      countRows -= removedRows;
    }
    return updatedTableData;
  };

  return (
    <>
      {tableData.length === 0 ? (
        <LoadingTable />
      ) : (
        <Stack sx={{ display: 'flex', justifyItems: 'center', alignItems: 'center', marginRight: 2 }}>
          {display && (
            <TableContainer sx={{ maxHeight: '1000px', maxWidth: '1000px' }} component={Paper}>
              <Table stickyHeader aria-label="collapsible table">
                <TableHead>
                  <TableRow sx={{ fontWeight: 'bold' }}>
                    <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)' }} />
                    <TableCell align="center" sx={{ backgroundColor: 'rgb(33, 150, 243,0.8)' }}>
                      <Button
                        id="clearAll"
                        variant="outlined"
                        onClick={clearAll}
                        sx={{ color: 'black', fontWeight: 'bold', fontSize: '18px', flexDirection: 'column' }}
                      >
                        <Typography variant="subtitle1" sx={{ color: 'white', lineHeight: '1' }}>
                          Fixed budget
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{ color: '', fontSize: '10px', fontWeight: 'bold', lineHeight: '2' }}
                        >
                          (Clear All)
                        </Typography>
                      </Button>
                    </TableCell>
                    <TableCell
                      sx={{
                        backgroundColor: 'rgb(33, 150, 243,0.8)',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '18px',
                      }}
                      align="center"
                    >
                      Subject
                    </TableCell>
                    <TableCell
                      sx={{
                        backgroundColor: 'rgb(33, 150, 243,0.8)',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '18px',
                      }}
                      align="center"
                    >
                      Budget
                    </TableCell>

                    <TableCell
                      sx={{
                        backgroundColor: 'rgb(33, 150, 243,0.8)',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '18px',
                      }}
                      align="center"
                    >
                      Vote
                    </TableCell>
                    <TableCell
                      sx={{
                        backgroundColor: 'rgb(33, 150, 243,0.8)',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '18px',
                      }}
                      align="center"
                    >
                      Precent
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {tableData.map((row) => (
                    <Row
                      key={row.id}
                      parent={tableData}
                      row={row}
                      handleVote={handleVote}
                      updateBudget={updateBudget}
                      handleCheckBox={handleCheckBox}
                      totalBudget={maxBudget}
                      newMaxBudget={newMaxBudget}
                      maxBudget={maxBudget}
                    />
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          <PopCardSubmit setDisplay={setDisplay} allData={{ ...allData, children: tableData }} />
        </Stack>
      )}
    </>
  );
}