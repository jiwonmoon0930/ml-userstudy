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
  fetch('http://localhost:8080/setup')
    .then(response => response.json())
    .then(data => {
      console.log(data)
      console.log(data['task_number']);
      // send user id as well
      setTmpUser(data['user_id'])
      });
  }, []);
    

  return (
    <div className="container"> 
      <Form form={form} layout='vertical' onFinish={onFinish}>
        <div className="title"> Study survey</div>
        <Form.Item 
            name="Q1" 
            label="1. How confident were you in your responses to complete the task?"
            rules={[{ required: true, message: "Please select an option!" }]}>
            <Radio.Group>
                <Radio value="1">Very unconfident</Radio>
                <Radio value="2">Unconfident</Radio>
                <Radio value="3">Average</Radio>
                <Radio value="4">Confident</Radio>
                <Radio value="5">Very confident</Radio>
            </Radio.Group>
        </Form.Item>

        <Form.Item 
            name="Q2" 
            label="2. How much did you rely on the AI's suggestion?"
            rules={[{ required: true, message: "Please select an option!" }]}>
            <Radio.Group>
                <Radio value="1">Very unrelient</Radio>
                <Radio value="2">Unrelient</Radio>
                <Radio value="3">Average</Radio>
                <Radio value="4">Relient</Radio>
                <Radio value="5">Very Relient</Radio>
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