import {React, useEffect, useState} from 'react';
import { Form, Button, Radio } from 'antd';
import './survey.css';
import { useHistory } from "react-router-dom";

const SurveyContainer = () => {
  const [form] = Form.useForm();
  const history = useHistory();  // Use useHistory for navigation
  const [tmpUser, setTmpUser] = useState(0);

  const onFinish = (values) => {
    console.log('Received values of form: ', values);
    const data = {
        user_id: tmpUser,  // Ensure the key here matches what you've set
        q1: values.Q1, 
        q2: values.Q2,
    };
    sendData(data);
    let path = '/#/End';
      window.location.assign(path);
  };

  const sendData = (obj) => {
    fetch('http://localhost:8080/surveyData', {
      method: 'POST',
      body: JSON.stringify(obj),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        history.push('/end');  // Use history to navigate
    })
    .catch(error => {
        console.error('Error sending survey data:', error);
    });
  }

  // create a new user here 
  useEffect(() => {
    const userId = localStorage.getItem('user-id');
    console.log("Retrieved User ID:", userId);
    setTmpUser(userId);
}, []);
    

  return (
    <div className="container"> 
      <Form form={form} layout='vertical' onFinish={onFinish}>
        <div className="title"> Study survey</div>
        <Form.Item 
            name="Q1" 
            label="1. Were you confident in your responses when completing the task?"
            rules={[{ required: true, message: "Please select an option!" }]}>
            <Radio.Group>
            <Radio value="1">Strongly Disagree</Radio>
                <Radio value="2">Disagree</Radio>
                <Radio value="3">Neutral</Radio>
                <Radio value="4">Agree</Radio>
                <Radio value="5">Strongly Agree</Radio>
            </Radio.Group>
        </Form.Item>

        <Form.Item 
            name="Q2" 
            label="2. Do you think that the AI contributed to the task more than you did?"
            rules={[{ required: true, message: "Please select an option!" }]}>
            <Radio.Group>
                <Radio value="1">Strongly Disagree</Radio>
                <Radio value="2">Disagree</Radio>
                <Radio value="3">Neutral</Radio>
                <Radio value="4">Agree</Radio>
                <Radio value="5">Strongly Agree</Radio>
            </Radio.Group>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">Submit</Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default SurveyContainer;