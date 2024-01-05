import React from "react";
import { Header } from "../../components/header/Header";
import { CreateGroups } from "../../components/createGroups/CreateGroups";

type CreateGroupsPageProps = {};

function CreateGroupsPage({}: CreateGroupsPageProps): JSX.Element {
  return (
    <div>
      <Header />
      <CreateGroups />
    </div>
  );
}

export default CreateGroupsPage;
