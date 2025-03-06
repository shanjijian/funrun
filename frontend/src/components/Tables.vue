<template>
  <el-container class="layout-container-demo" style="height: 750px">
    <el-aside width="200px" style="position: absolute; left: 0; top: 0;">
      <el-scrollbar>
        <el-menu :default-openeds="['1', '1']" @select="handleMenuSelect">
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <icon-menu/>
              </el-icon>
              函数操作
            </template>
            <el-menu-item-group>
              <el-menu-item index="list">列表</el-menu-item>
              <el-menu-item index="add">增加</el-menu-item>
              <el-menu-item index="update">修改</el-menu-item>
            </el-menu-item-group>
            <el-menu-item index="execute">执行</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <el-icon>
                  <DocumentCopy/>
                </el-icon>
              </el-icon>
              Yaml操作
            </template>
            <el-menu-item-group>
              <el-menu-item index="yamlList">列表</el-menu-item>
              <el-menu-item index="yamlAdd">增加</el-menu-item>
              <el-menu-item index="yamlUpdate">修改</el-menu-item>
            </el-menu-item-group>
            <el-menu-item index="yamlExecute">执行</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-main style="display: flex; justify-content: center;">
        <!-- 列表 -->
        <el-card v-if="selectedMenu === 'list'" style="width: 800px;">
          <h2>函数列表</h2>
          <el-scrollbar>
            <el-table :data="functionsList">
              <el-table-column prop="rule_name" label="规则名称" width="140"/>
              <el-table-column prop="function_name" label="函数名称" width="140"/>
              <el-table-column prop="function_code" label="代码" show-overflow-tooltip width="340"/>
              <el-table-column label="操作" width="140">
                <template #default="{ row }">
                  <el-button type="danger" @click="deleteFunction(row.function_name)" size="small">删除</el-button>
                  <el-button type="warning" @click="editFunction(row)" size="small">编辑</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-scrollbar>
        </el-card>


        <el-card v-if="selectedMenu === 'yamlList'" style="width: 800px;">
          <h2>Yaml列表</h2>
          <el-scrollbar>
            <el-table :data="yamlList">
              <el-table-column prop="rule_name" label="规则名称" width="140"/>
              <el-table-column prop="yaml_name" label="yaml名称" width="140"/>
              <el-table-column prop="yaml_code" label="代码" show-overflow-tooltip width="340"/>
              <el-table-column label="操作" width="140">
                <template #default="{ row }">
                  <el-button type="danger" @click="deleteYaml(row.yaml_name)" size="small">删除</el-button>
                  <el-button type="warning" @click="editYaml(row)" size="small">编辑</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-scrollbar>
        </el-card>


        <!-- 添加 -->
        <el-card v-if="selectedMenu === 'add'" style="width: 800px;">
          <h2>添加函数</h2>
          <el-form :model="form" label-width="auto" style="max-width: 100%">
            <el-form-item label="规则名称">
              <el-input v-model="form.ruleName" placeholder="请输入规则名称"/>
            </el-form-item>
            <el-form-item label="函数名称">
              <el-input v-model="form.functionName" placeholder="请输入函数名称"/>
            </el-form-item>
            <el-form-item label="函数代码">
              <el-input v-model="form.functionCode" type="textarea" placeholder="请输入函数代码"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addFunction">添加函数</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 添加 -->
        <el-card v-if="selectedMenu === 'yamlAdd'" style="width: 800px;">
          <h2>添加Yaml</h2>
          <el-form :model="yamlForm" label-width="auto" style="max-width: 100%">
            <el-form-item label="规则名称">
              <el-input v-model="yamlForm.ruleName" placeholder="请输入规则名称"/>
            </el-form-item>
            <el-form-item label="Yaml名称">
              <el-input v-model="yamlForm.yamlName" placeholder="请输入Yaml名称"/>
            </el-form-item>
            <el-form-item label="Yaml代码">
              <el-input v-model="yamlForm.yamlCode" type="textarea" placeholder="请输入Yaml代码"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addYaml">添加Yaml</el-button>
            </el-form-item>
          </el-form>
        </el-card>


        <!-- 更新 -->
        <el-card v-if="selectedMenu === 'update'" style="width: 800px;">
          <h2>更新函数代码</h2>
          <el-form :model="form" label-width="auto" style="max-width: 100%">
            <el-form-item label="函数名称">
              <el-input v-model="form.functionName" placeholder="函数名称"/>
            </el-form-item>
            <el-form-item label="新函数代码">
              <el-input v-model="form.functionCode" type="textarea" placeholder="请输入新函数代码"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updateFunction">更新代码</el-button>
            </el-form-item>
          </el-form>
        </el-card>


        <!-- 更新 -->
        <el-card v-if="selectedMenu === 'yamlUpdate'" style="width: 800px;">
          <h2>更新Yaml代码</h2>
          <el-form :model="yamlForm" label-width="auto" style="max-width: 100%">
            <el-form-item label="Yaml名称">
              <el-input v-model="yamlForm.yamlName" placeholder="Yaml名称"/>
            </el-form-item>
            <el-form-item label="新Yaml代码">
              <el-input v-model="yamlForm.yamlCode" type="textarea" placeholder="请输入新Yaml代码"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updateYaml">更新Yaml</el-button>
            </el-form-item>
          </el-form>
        </el-card>


        <!-- 执行 -->
        <el-card v-if="selectedMenu === 'execute'" style="width: 800px;">
          <h2>执行任务</h2>
          <el-form :model="form" label-width="auto" style="max-width: 100%">
            <el-form-item label="任务名称">
              <el-input v-model="form.taskName" placeholder="任务名称 (例如 es_dsl_verification)"/>
            </el-form-item>
            <el-form-item label="任务数据">
              <el-input v-model="form.taskData" type="textarea" placeholder="任务数据 (JSON 格式)"/>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="executeTask">执行任务</el-button>
            </el-form-item>
          </el-form>
        </el-card>


        <el-card v-if="selectedMenu === 'yamlExecute'" style="width: 800px;">
          <h2>执行Yaml</h2>
          <el-form :model="yamlForm" label-width="auto" style="max-width: 100%">
            <el-form-item label="Yaml名称">
              <el-input v-model="yamlForm.taskName" placeholder="任务名称 (例如 test)"/>
            </el-form-item>
            <el-form-item label="任务数据">
              <el-input v-model="yamlForm.taskData" type="textarea" placeholder="任务数据 (JSON 格式)"/>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="yamlTask">执行任务</el-button>
            </el-form-item>
          </el-form>
        </el-card>

      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import {onMounted, ref, watch} from 'vue'
import {DocumentCopy, Menu as IconMenu} from '@element-plus/icons-vue'
import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";

// form model
const form = ref({
  ruleName: '',
  functionName: '',
  functionCode: '',
  taskName: '',
  taskData: ''
});


const yamlForm = ref({
  ruleName: '',
  yamlName: '',
  yamlCode: '',
  taskName: '',
  taskData: ''
});

const selectedMenu = ref('list');
const ruleName = ref('');
const functionName = ref('');
const code = ref('');
const taskName = ref('');
const taskData = ref('');
const functionsList = ref([]);

// load functions list
const loadFunctions = async () => {
  try {
    const response = await axios.get('http://10.95.14.174:8012/functions/list');
    functionsList.value = response.data;
  } catch (error) {
    ElMessage.error(`加载函数失败: ${error.response?.data?.detail || error.message}`);
  }
};


const yamlList = ref([]);

// 加载 YAML 配置列表
const loadYamlConfigs = async () => {
  try {
    const response = await axios.get('http://10.95.14.174:8012/yaml/list');
    yamlList.value = response.data;
  } catch (error) {
    ElMessage.error(`加载 YAML 失败: ${error.response?.data?.detail || error.message}`);
  }
};


// add function
const addFunction = async () => {
  try {
    await axios.post('http://10.95.14.174:8012/functions/add', {
      rule_name: form.value.ruleName,
      function_name: form.value.functionName,
      function_code: form.value.functionCode
    });
    ElMessage.success('函数添加成功');
    loadFunctions();
  } catch (error) {
    ElMessage.error(`添加函数失败: ${error.response?.data?.detail || error.message}`);
  }
};


// add function
const addYaml = async () => {
  try {
    await axios.post('http://10.95.14.174:8012/yaml/add', {
      rule_name: yamlForm.value.ruleName,
      yaml_name: yamlForm.value.yamlName,
      yaml_code: yamlForm.value.yamlCode
    });
    ElMessage.success('函数添加成功');
    loadYamlConfigs();
  } catch (error) {
    ElMessage.error(`添加函数失败: ${error.response?.data?.detail || error.message}`);
  }
};


// update function
const updateFunction = async () => {
  try {
    await axios.put('http://10.95.14.174:8012/functions/update', {
      identifier: form.value.functionName,
      new_code: form.value.functionCode,
      by_name: true
    });
    ElMessage.success('代码更新成功');
    loadFunctions();
  } catch (error) {
    ElMessage.error(`更新函数代码失败: ${error.response?.data?.detail || error.message}`);
  }
};

const updateYaml = async () => {
  try {
    await axios.put('http://10.95.14.174:8012/yaml/update', {
      identifier: yamlForm.value.yamlName,
      new_code: yamlForm.value.yamlCode,
      by_name: true
    });
    ElMessage.success('Yaml更新成功');
    loadYamlConfigs();
  } catch (error) {
    ElMessage.error(`Yaml代码失败: ${error.response?.data?.detail || error.message}`);
  }
};


// delete function
const deleteFunction = async (identifier) => {
  try {
    await ElMessageBox.confirm('确定删除该函数吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    await axios.delete('http://10.95.14.174:8012/functions/delete', {
      data: {identifier, by_name: true}
    });
    ElMessage.success('函数删除成功');
    loadFunctions();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`删除函数失败: ${error.response?.data?.detail || error.message}`);
    }
  }
};


const deleteYaml = async (identifier) => {
  try {
    await ElMessageBox.confirm('确定删除该函数吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    await axios.delete('http://10.95.14.174:8012/yaml/delete', {
      data: {identifier, by_name: true}
    });
    ElMessage.success('函数删除成功');
    loadYamlConfigs();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`删除函数失败: ${error.response?.data?.detail || error.message}`);
    }
  }
};


// execute task
const executeTask = async () => {
  try {
    const response = await axios.post('http://10.95.14.174:8012/execute', {
      rule_name: form.value.taskName,
      input_data: form.value.taskData
    });
    ElMessage.success(`任务执行成功: ${response.data.result}`);
  } catch (error) {
    ElMessage.error(`任务执行失败: ${error.response?.data?.detail || error.message}`);
  }
};


const yamlTask = async () => {
  try {
    const response = await axios.post('http://10.95.14.174:8012/yaml/execute', {
      rule_name: yamlForm.value.taskName,
      input_data: yamlForm.value.taskData
    });
    ElMessage.success(`任务执行成功: ${response.data.result}`);
  } catch (error) {
    ElMessage.error(`任务执行失败: ${error.response?.data?.detail || error.message}`);
  }
};


// handle menu selection
const handleMenuSelect = (index) => {
  selectedMenu.value = index;
};


// 编辑函数时填充表单
const editFunction = (row: any) => {
  form.value.ruleName = row.rule_name;
  form.value.functionName = row.function_name;
  form.value.functionCode = row.function_code;
  selectedMenu.value = 'update';
};

// 编辑 YAML 时填充表单
const editYaml = (row: any) => {
  yamlForm.value.ruleName = row.rule_name;
  yamlForm.value.yamlName = row.yaml_name;
  yamlForm.value.yamlCode = row.yaml_code;
  selectedMenu.value = 'yamlUpdate';
};

// 监听 selectedMenu，切换时重置表单，防止旧数据残留
watch(selectedMenu, () => {
  resetForm();
  resetYamlForm();
});

// 重置表单
const resetForm = () => {
  form.value = {
    ruleName: '',
    functionName: '',
    code: '',
    taskName: '',
    taskData: ''
  };
};

// 重置 YAML 表单
const resetYamlForm = () => {
  yamlForm.value = {
    ruleName: '',
    yamlName: '',
    yamlCode: '',
    taskName: '',
    taskData: ''
  };
};


onMounted(loadFunctions);
onMounted(loadYamlConfigs);
</script>

<style scoped>
.el-card {
  box-shadow: none !important;
}
</style>
