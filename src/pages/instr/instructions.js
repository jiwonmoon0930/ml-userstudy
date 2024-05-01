import React, { Component,useState, useEffect } from "react";
import {Button, Modal, Checkbox} from 'antd'
import "./instructions.css";

function InstructionsContainer() {

    const [agree, setAgree] = useState(false);
    const [task, setTask] = useState(0);

    const checkboxHandler = () => {
        setAgree(!agree);
    }

    const routeChange = () =>{ 
        if (task == 1) {
            let path = '/#/Main1';
            window.location.assign(path);
        } else if (task == 2) {
            let path = '/#/Main2';
            window.location.assign(path);
        } else {
            let path = '/#/Main3';
            window.location.assign(path);
        }
    }

    // connect with the backend to randomize the task 
    useEffect(() => {
        fetch('http://localhost:8080/setup')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            console.log(data['task_number']);
            setTask(data['task_number']);
            // send user id as well
            localStorage.setItem('user-id', data['user_id']);
            console.log(localStorage)
        });
    }, []);


    return (
      <div className="instr-container">
        <h1 className="instr-title">
            Instructions
        </h1> 

        <div className="instr-text"> 
            You have recently relocated to a new city and are in the process of furnishing your new apartment.
            You will be using a second-hand marketplace website to find various pieces of furniture such as chairs,
            tables, lamps, bed frames, drawers, etc. For each item, we will provide you with information of the item.
            Your task is to evaluate each item based on the provided information and decide whether or not you would trust the seller.
        </div>

        <div className="instr-text"> 
            <Checkbox onChange={checkboxHandler} style={{fontSize:"20px", textAlign: 'left', alignSelf: 'stretch'}}>
                I've understand the task.
            </Checkbox> 
        </div>

        <div className="instr-text"> 
            <Button disabled={!agree} variant="btn btn-success" onClick={routeChange}>
                Start
            </Button>
        </div>

      </div>
      );
}

export default InstructionsContainer;