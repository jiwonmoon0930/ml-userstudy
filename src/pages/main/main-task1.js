import React, { Component, useState, useEffect } from "react";
import {Button, Modal, Checkbox, Input, Radio} from 'antd'
import "antd/dist/antd.css";
import "./main-task1.css";

function Main1Container() {
    const [text, setText] = useState("");
    const [task, setTask] = useState(0);
    const [choice, setChoice] = useState(0);
    const [tmpUser, setTmpUser] = useState(0);
    const [imageData, setImageData] = useState([]);
    const [currentImage, setCurrentImage] = useState("");
    const [currentName, setCurrentName] = useState("");
    const [currentUser, setCurrentUser] = useState("");
    const [currentPrice, setCurrentPrice] = useState("");
    const [currentDescription, setCurrentDescription] = useState("");
    const [imageCount, setImageCount] = useState(0);
    const [taskTime, setTaskTime] = useState(null);

    const [currentTime, setCurrentTime] = useState(0);
    const [moveToSurvey, setMoveToSurvey] = useState(false);

    const [render, setRender] = useState(false);

    let totalImages = 16;
    const baseImgUrl = "./images/";

    const nextChange = () =>{
        if (choice<1) {
            alert("Please make sure to complete all the fields!");
        } else {
            let count = imageCount + 1;
            // save data
            let data = {
                q_id: currentImage,
                user_id: tmpUser,
                ans: choice,
                input: text, 
                time: ((Date.now() - taskTime) / 1000).toFixed(3)
            };
            console.log(data)
            sendData(data)
            if (count >= totalImages) {
                console.log('done with images')
                setMoveToSurvey(true);
                let path = '/#/Survey'; 
                window.location.assign(path);
            } else {
                // reinitialize variables
                setChoice(0); 
                setText("")
                setImageCount(count);
                setCurrentImage(imageData[count].name);
                setCurrentName(imageData[count].label);
                setCurrentUser(imageData[count].user);
                setCurrentPrice(imageData[count].price);
                setCurrentDescription(imageData[count].description);
                setTaskTime(Date.now())
            }
        }
    }

    const sendData = (obj) => {
        fetch('http://localhost:8080/responsesData', {
          method: 'POST',
          body: JSON.stringify(obj),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        }).then(response => response.json())
          .then(message => {
            console.log(message)
          })
      } 


    const onChangeMultiple= e => {
        setChoice(e.target.value);

    };

    // testing communication with backend
    useEffect(() => {
        fetch('http://0.0.0.0:8080/time').then(res => 
        res.json()).then(data => {
            setCurrentTime(data.time);
            console.log(data.time)
        });
        }, []);

    // create a new user here 
    useEffect(() => {
        fetch('http://localhost:8080/setup')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            console.log(data['task_number']);
            setTask(data['task_number']);
            // send user id as well
            setTmpUser(data['user_id'])
        });
    }, []);
    

    // initialize image
    useEffect(() => {
        console.log('getting images')
        fetch('http://localhost:8080/imageInfo')
        .then(response => response.json())
        .then(data => {
            console.log(data['imgs']);
            setImageData(data['imgs']);
            let image_name = data['imgs'][0].name
            setCurrentImage(image_name)
            console.log(image_name)
            setCurrentName(data['imgs'][0].label);
            setCurrentUser(data['imgs'][0].user);
            setCurrentPrice(data['imgs'][0].price);
            setCurrentDescription(data['imgs'][0].description);
            setRender(true);
            setTaskTime(Date.now())
        });
    }, []);


    return (
      <>
       {render ?
            <div className="task-container">
                <div className="column-container"> 
                    <div className="left-column"> 
                        <div className="task-img-frame">
                            <img className="image-inner" src={baseImgUrl + currentImage}/>
                        </div>
                    </div>

                    <div className="right-column"> 
                        <div className="item-title">
                            {currentName}
                        </div>
                        <div className="item-user">
                            <img className="item-user-icon" src={baseImgUrl+"user.png"}/>
                            {" " + currentUser}
                        </div>
                        <div className="item-price">
                            {currentPrice}
                        </div>
                        <div className="item-description">
                            {"\"" + currentDescription + "\""}
                        </div>
                    </div>
                </div>

                <div className="question-container">
                    <div className="question">
                        <t> Can you trust the seller?</t>
                    </div>

                    <Radio.Group onChange={onChangeMultiple} value={choice}>
                        <Radio value={1}> <t>Yes</t> </Radio>
                        <Radio value={2}> <t>Not sure</t> </Radio>
                        <Radio value={3}> <t>No</t> </Radio>
                    </Radio.Group>
                </div>

                <div className="button-container"> 
                    <Button variant="btn btn-success" onClick={nextChange}>
                        Next
                    </Button>
                </div>

            {(moveToSurvey) && 
            <div className="instr"> 
                <t> You have completed the three tasks. </t>
                
            </div>
            }

            </div>

        :
            <> 
            <h1> Loading ...</h1>
            </>
        }
      </>
       
      );
}

export default Main1Container;