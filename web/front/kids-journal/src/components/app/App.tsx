import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { AppRoute } from "../../const";
import "../../static/css/global.css";
import WelcomeScreen from "../../pages/welcome-screen/welcome-screen";
import GroupsPage from "../../pages/groups-page/GroupsPage";
import MainPage from "../../pages/main-page/MainPage";
import GroupInfoPage from "../../pages/groupInfo-page/GroupInfoPage";
import EmployeesPage from "../../pages/employees-page/EmployeesPage";
import CreateEmployeesPage from "../../pages/createEmployees-page/CreateEmployeesPage";
import AddChildPage from "../../pages/addChild-page/AddChildPage";
import ActivityPage from "../../pages/activity-page/ActivityPage";
import CreateGroupsPage from "../../pages/createGroups-page/CreateGroupsPage";
import { Header } from "../header/Header";
import CreateActivityPage from "../../pages/createActivity-page/CreateActivityPage";
import { SubjectPage } from "../../pages/subject-page/SubjectPage";
import CreateSubjectPage from "../../pages/creactSubject-page/CreateSubjectPage";

function App() {
  return (
    <div className="app_container">
      <Router>
        <Routes>
          <Route path={AppRoute.WelcomeScreen} element={<WelcomeScreen />} />
          <Route
            path={`:organization${AppRoute.Main}`}
            element={<MainPage />}
          />
          <Route
            path={`:organization${AppRoute.Groups}`}
            element={<GroupsPage />}
          />
          <Route path={`:organization/:groupId`} element={<GroupInfoPage />} />
          <Route
            path={`:organization${AppRoute.Employees}`}
            element={<EmployeesPage />}
          />
          <Route
            path={`:organization${AppRoute.Activity}`}
            element={<ActivityPage />}
          />
          <Route path={AppRoute.CreateGroups} element={<CreateGroupsPage />} />
          <Route
            path={AppRoute.CreateEmployees}
            element={<CreateEmployeesPage />}
          />
          <Route path={`${AppRoute.AddChild}`} element={<AddChildPage />} />

          <Route
            path={`:organization${AppRoute.Subject}`}
            element={<SubjectPage />}
          />

          <Route
            path={`:organization${AppRoute.CreateSubject}`}
            element={<CreateSubjectPage />}
          />

          <Route
            path={`:organization${AppRoute.CreateActivity}`}
            element={<CreateActivityPage />}
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
