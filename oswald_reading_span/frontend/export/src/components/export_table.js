import "./export_table.css";

import React from "react";
import autoBind from "auto-bind";
import { DataTable } from "./datatable";
import NetworkProgressBar from "./network_progress_bar";

export default class RSPANResultTable extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.dataTableRef = React.createRef();

    this.state = {
      hasData: false,
      data: null,
      currentPage: 0,
    };
  }

  render() {
    return (
      <div
        className={"experiment-test-datatable"}
        id={"experiment-test-datatable"}
      >
        <div
          className={
            this.state.hasData
              ? "progress-bar-container hidden"
              : "progress-bar-container"
          }
        >
          <h1 className="progress-bar-title">
            Loading subject data, please wait...
          </h1>
          <NetworkProgressBar
            initiateDataLoad={this.props.initiateDataLoad}
            onDataLoaded={this.onDataLoaded}
          />
        </div>
        <DataTable
          columnNames={["ID", "Timestamp", "Subject ID", "Experiment Version"]}
          columns={["id", "timestamp", "subject_id", "experiment_version"]}
          tableData={this.state.data}
          hasData={this.state.hasData}
          tableId={"experiment-test-table"}
          selectStyle={this.props.selectStyle}
          onRowSelected={this.props.onRowSelected}
          ref={this.dataTableRef}
        />
        <button
          id={this.state.hasData ? "export-button" : "export-button-hidden"}
          onClick={this.props.onExportClicked}
        >
          Export
        </button>
      </div>
    );
  }

  onDataLoaded(data) {
    console.debug("export_table.onDataLoaded");
    console.debug(data);
    this.setState({
      hasData: true,
      data: data,
    });
  }

  getTable() {
    return this.dataTableRef.current;
  }
}
