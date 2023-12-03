import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { AppRoute } from "../../const";
import "../../static/css/global.css";
import WelcomeScreen from "../../pages/welcome-screen/welcome-screen";
import GroupsPage from "../../pages/groups-page/GroupsPage";
import MainPage from "../../pages/main-page/MainPage";
import GroupInfoPage from "../../pages/groupInfo-page/GroupInfoPage";
import EmployeesPage from "../../pages/employees-page/EmployeesPage";
import ActivityPage from "../../pages/activity-page/ActivityPage";
import CreateGroupsPage from "../../pages/createGroups-page/CreateGroupsPage";

function App() {
  return (
    <div className="app_container">
      <Router>
        <Routes>
          <Route path={AppRoute.WelcomeScreen} element={<WelcomeScreen />} />
          <Route path={AppRoute.Main} element={<MainPage />} />
          <Route path={AppRoute.Groups} element={<GroupsPage />} />
          <Route
            path={`${AppRoute.Groups}/:groupId`}
            element={<GroupInfoPage />}
          />
          <Route path={AppRoute.Employees} element={<EmployeesPage />} />
          <Route path={AppRoute.Activity} element={<ActivityPage />} />
          <Route path={AppRoute.CreateGroups} element={<CreateGroupsPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
