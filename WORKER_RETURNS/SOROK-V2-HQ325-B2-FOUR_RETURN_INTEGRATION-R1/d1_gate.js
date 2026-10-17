'use strict';
// Load the exact unchanged corrected D1 court, including its self-checks, in a VM.
const fs=require('fs'), vm=require('vm'), crypto=require('crypto');
const source=fs.readFileSync(process.argv[2],'utf8');
const packet=JSON.parse(fs.readFileSync(0,'utf8'));
let failures=[];
const sandbox={console:{log:()=>{},error:(...x)=>failures.push(x)},process:{exitCode:0}};
vm.createContext(sandbox);
vm.runInContext(source,sandbox,{timeout:1000});
if(failures.length || sandbox.process.exitCode)throw Error('D1_FROZEN_SELF_TEST_FAILURE');
sandbox.__input=JSON.stringify(packet);
const result=vm.runInContext('judge(JSON.parse(__input))',sandbox,{timeout:1000});
process.stdout.write(JSON.stringify({result,source_sha256:crypto.createHash('sha256').update(source).digest('hex'),self_tests:17}));
